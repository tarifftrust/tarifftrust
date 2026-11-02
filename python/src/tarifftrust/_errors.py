"""What a call may raise: the API's refusals by their status, and the failures to reach it."""

from __future__ import annotations

from typing import Any


class TariffTrustError(Exception):
    """What a call raises when the API refuses it or cannot be reached. An argument that cannot
    be sent at all is a ``TypeError`` or a ``ValueError``, before any request."""


class APIConnectionError(TariffTrustError):
    """The API could not be reached, after the retries."""


class APITimeoutError(APIConnectionError):
    """The API did not answer in time, after the retries."""


class APIError(TariffTrustError):
    """The API refused the request. ``code`` is for a program, ``message`` for a person,
    ``fields`` names what invalid_input refused, ``request_id`` is what to quote to support, and
    ``retry_after`` the seconds to wait when trying again helps, None otherwise."""

    def __init__(
        self,
        message: str,
        *,
        status: int,
        code: str | None = None,
        fields: list[str] | None = None,
        request_id: str | None = None,
        retry_after: int | None = None,
        body: Any = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status = status
        self.code = code
        self.fields = fields or []
        self.request_id = request_id
        self.retry_after = retry_after
        self.body = body

    def __str__(self) -> str:
        details = [f"HTTP {self.status}"]
        if self.fields:
            details.append("fields: " + ", ".join(self.fields))
        if self.request_id:
            details.append(f"request {self.request_id}")
        prefix = f"{self.code}: " if self.code else ""
        return f"{prefix}{self.message} ({'; '.join(details)})"


class AuthenticationError(APIError):
    """401: no valid API key."""


class AccessRequiredError(APIError):
    """402: no active subscription, or the quota is used up (code ``quota_exceeded``)."""


class PermissionDeniedError(APIError):
    """403: the key lacks the permission, or the plan the API."""


class NotFoundError(APIError):
    """404: nothing of that name."""


class ConflictError(APIError):
    """409: an idempotency key sent again with another request."""


class PayloadTooLargeError(APIError):
    """413: the body is larger than the API takes: send fewer products or lines."""


class InvalidInputError(APIError):
    """422: ``fields`` names each field refused; 400: the body is not valid JSON."""


class RateLimitError(APIError):
    """429: too many requests."""


class ServiceUnavailableError(APIError):
    """502, 503 or 504: unavailable for now."""


BY_STATUS: dict[int, type[APIError]] = {
    400: InvalidInputError,
    401: AuthenticationError,
    402: AccessRequiredError,
    403: PermissionDeniedError,
    404: NotFoundError,
    409: ConflictError,
    413: PayloadTooLargeError,
    422: InvalidInputError,
    429: RateLimitError,
    502: ServiceUnavailableError,
    503: ServiceUnavailableError,
    504: ServiceUnavailableError,
}
