"""The clients: the key, the retries, the idempotency key and the errors around each operation."""

from __future__ import annotations

import asyncio
import json
import os
import platform
import random
import time
import uuid
from collections.abc import Mapping
from datetime import date
from decimal import Decimal
from types import TracebackType
from typing import Any, TypeVar

import httpx

from ._errors import (
    BY_STATUS,
    APIConnectionError,
    APIError,
    APITimeoutError,
    AuthenticationError,
    TariffTrustError,
)
from ._model import Model
from ._operations import AsyncOperations, Operations
from ._version import __version__

DEFAULT_BASE_URL = "https://api.tarifftrust.com"
DEFAULT_TIMEOUT = 60.0
DEFAULT_MAX_RETRIES = 2
DEFAULT_MAX_RETRY_WAIT = 60.0
# What a gateway answers when the service behind it is away, without the API's error.
GATEWAY_STATUSES = {429, 502, 503, 504}
USER_AGENT = f"tarifftrust-python/{__version__} python/{platform.python_version()}"
_M = TypeVar("_M", bound=Model)


def _encode(value: Any) -> str:
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, date):
        return value.isoformat()
    raise TypeError(f"{type(value).__name__} cannot be sent to the API")


def _sent(fields: Mapping[str, Any] | None) -> dict[str, Any]:
    """The arguments given: one left at None is not sent, and the API takes its default."""
    return {name: value for name, value in (fields or {}).items() if value is not None}


def _retry_after(response: httpx.Response) -> int | None:
    value = response.headers.get("Retry-After", "")
    return int(value) if value.isdigit() else None


def _error(response: httpx.Response) -> APIError:
    try:
        body = response.json()
    except ValueError:
        body = None
    error = body.get("error") if isinstance(body, dict) else None
    # The admin-style error of a proxy may be a plain string: only an object is the API's.
    error = error if isinstance(error, dict) else {}
    kind = BY_STATUS.get(response.status_code, APIError)
    return kind(
        error.get("message") or f"HTTP {response.status_code}",
        status=response.status_code,
        code=error.get("code"),
        fields=error.get("fields"),
        request_id=(body.get("request_id") if isinstance(body, dict) else None)
        or response.headers.get("X-Request-ID"),
        retry_after=_retry_after(response),
        body=body,
    )


def _backoff(attempt: int) -> float:
    return min(0.5 * float(2**attempt), 8.0) * random.uniform(0.5, 1.0)


def _wait_before_retry(error: APIError, attempt: int, longest: float) -> float | None:
    """How long to wait before trying again, None when trying again cannot help. The API says so
    by its Retry-After: a refusal without one stays refused, and one too long is the caller's."""
    if error.retry_after is not None:
        return float(error.retry_after) if error.retry_after <= longest else None
    if error.code is None and error.status in GATEWAY_STATUSES:
        return _backoff(attempt)
    return None


def _answer(response: httpx.Response, model: type[_M]) -> _M:
    try:
        return model(response.json())
    except ValueError as exc:
        status = response.status_code
        raise TariffTrustError(f"The API's answer is not JSON (HTTP {status})") from exc


def _unreachable(exc: httpx.RequestError) -> APIConnectionError:
    if isinstance(exc, httpx.TimeoutException):
        return APITimeoutError(f"The API did not answer in time: {exc}")
    return APIConnectionError(f"The API could not be reached: {exc}")


class _Settings:
    def __init__(
        self,
        api_key: str | None,
        base_url: str | None,
        timeout: float,
        max_retries: int,
        max_retry_wait: float,
    ) -> None:
        # A stray newline would be refused as a header, with the key in the message.
        self.api_key = (api_key or os.environ.get("TARIFFTRUST_API_KEY") or "").strip() or None
        self.timeout = timeout
        found = base_url or os.environ.get("TARIFFTRUST_BASE_URL") or DEFAULT_BASE_URL
        self.base_url = found.rstrip("/")
        self.max_retries = max_retries
        self.max_retry_wait = max_retry_wait

    def request(
        self,
        method: str,
        path: str,
        *,
        query: Mapping[str, Any] | None,
        body: Mapping[str, Any] | None,
        auth: bool,
        idempotent: bool,
        idempotency_key: str | None,
    ) -> dict[str, Any]:
        """What each attempt of a call sends: the idempotency key is the call's, so that a retry
        counts once."""
        headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
        if auth:
            if not self.api_key:
                raise AuthenticationError(
                    "No API key: pass api_key or set TARIFFTRUST_API_KEY", status=401
                )
            headers["Authorization"] = f"Bearer {self.api_key}"
        if idempotent:
            if idempotency_key and not idempotency_key.isascii():
                raise ValueError("An idempotency key is a header: use only ASCII characters")
            headers["Idempotency-Key"] = idempotency_key or str(uuid.uuid4())
        request: dict[str, Any] = {
            "method": method,
            "url": self.base_url + path,
            "headers": headers,
            "params": _sent(query),
            "timeout": self.timeout,
        }
        if body is not None:
            headers["Content-Type"] = "application/json"
            request["content"] = json.dumps(_sent(body), default=_encode)
        return request

    def wait_after_failure(self, failure: httpx.RequestError, attempt: int) -> float:
        """The seconds before trying again after a failure to reach the API, or what it raises."""
        if attempt >= self.max_retries:
            raise _unreachable(failure) from failure
        return _backoff(attempt)

    def wait_after_refusal(self, response: httpx.Response, attempt: int) -> float:
        """The seconds before trying again after a refusal, or the error the call ends with."""
        error = _error(response)
        wait = _wait_before_retry(error, attempt, self.max_retry_wait)
        if wait is None or attempt >= self.max_retries:
            raise error
        return wait


class TariffTrust(Operations):
    """The TariffTrust API. Each operation of the API is a method under its operationId.

    Args:
        api_key: The key, or TARIFFTRUST_API_KEY. Keep it on your server. Only ``get_status``
            works without one.
        base_url: The API's address, or TARIFFTRUST_BASE_URL; the production's otherwise.
        timeout: The seconds to wait at each step of an attempt: connecting, sending, each read.
            It applies to your own ``http_client`` too.
        max_retries: How many times a call is tried again: after a connection failure, a timeout
            or a gateway error, or when the API gives a Retry-After. An idempotency key makes these
            retries count once.
        max_retry_wait: The longest Retry-After waited for, in seconds; a longer one is raised.
        http_client: Your own ``httpx.Client`` (a proxy, your certificates): yours to close.
    """

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str | None = None,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        max_retry_wait: float = DEFAULT_MAX_RETRY_WAIT,
        http_client: httpx.Client | None = None,
    ) -> None:
        self._settings = _Settings(api_key, base_url, timeout, max_retries, max_retry_wait)
        self._owns_http = http_client is None
        self._http = http_client or httpx.Client()

    def _request(
        self,
        method: str,
        path: str,
        *,
        model: type[_M],
        query: Mapping[str, Any] | None = None,
        body: Mapping[str, Any] | None = None,
        auth: bool = True,
        idempotent: bool = False,
        idempotency_key: str | None = None,
    ) -> _M:
        settings = self._settings
        request = settings.request(
            method,
            path,
            query=query,
            body=body,
            auth=auth,
            idempotent=idempotent,
            idempotency_key=idempotency_key,
        )
        attempt = 0
        while True:
            try:
                response = self._http.request(**request)
            except httpx.RequestError as exc:
                wait = settings.wait_after_failure(exc, attempt)
            else:
                if response.is_success:
                    return _answer(response, model)
                wait = settings.wait_after_refusal(response, attempt)
            time.sleep(wait)
            attempt += 1

    def close(self) -> None:
        """Close the connections; your own ``http_client`` stays open."""
        if self._owns_http:
            self._http.close()

    def __enter__(self) -> TariffTrust:
        return self

    def __exit__(
        self,
        kind: type[BaseException] | None,
        value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()


class AsyncTariffTrust(AsyncOperations):
    """The TariffTrust API for ``asyncio``: the methods and arguments of ``TariffTrust``, awaited.
    ``http_client`` is your own ``httpx.AsyncClient``: yours to close."""

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str | None = None,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        max_retry_wait: float = DEFAULT_MAX_RETRY_WAIT,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        self._settings = _Settings(api_key, base_url, timeout, max_retries, max_retry_wait)
        self._owns_http = http_client is None
        self._http = http_client or httpx.AsyncClient()

    async def _request(
        self,
        method: str,
        path: str,
        *,
        model: type[_M],
        query: Mapping[str, Any] | None = None,
        body: Mapping[str, Any] | None = None,
        auth: bool = True,
        idempotent: bool = False,
        idempotency_key: str | None = None,
    ) -> _M:
        settings = self._settings
        request = settings.request(
            method,
            path,
            query=query,
            body=body,
            auth=auth,
            idempotent=idempotent,
            idempotency_key=idempotency_key,
        )
        attempt = 0
        while True:
            try:
                response = await self._http.request(**request)
            except httpx.RequestError as exc:
                wait = settings.wait_after_failure(exc, attempt)
            else:
                if response.is_success:
                    return _answer(response, model)
                wait = settings.wait_after_refusal(response, attempt)
            await asyncio.sleep(wait)
            attempt += 1

    async def close(self) -> None:
        """Close the connections; your own ``http_client`` stays open."""
        if self._owns_http:
            await self._http.aclose()

    async def __aenter__(self) -> AsyncTariffTrust:
        return self

    async def __aexit__(
        self,
        kind: type[BaseException] | None,
        value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.close()
