"""What each call sends, when it is tried again, and what it raises."""

import asyncio
import json
from datetime import date
from decimal import Decimal
from pathlib import Path

import httpx
import pytest

import tarifftrust
from tarifftrust import (
    AccessRequiredError,
    APIConnectionError,
    APIError,
    APITimeoutError,
    AsyncTariffTrust,
    AuthenticationError,
    ConflictError,
    InvalidInputError,
    NotFoundError,
    PayloadTooLargeError,
    PermissionDeniedError,
    RateLimitError,
    ServiceUnavailableError,
    TariffTrust,
    TariffTrustError,
)

REFUSED = {"error": {"code": "rate_limited", "message": "Too many requests"}, "request_id": "r-1"}
ROOT = Path(__file__).resolve().parents[2]


def test_a_call_sends_the_key_and_only_the_arguments_given(api, client):
    api.answer(body={"status": "calculated", "estimated_duty": "2400.00"})
    result = client.estimate(hts="6109.10.00.12", origin="CN", customs_value="10000")
    request = api.requests[0]
    assert (request.method, str(request.url)) == (
        "POST",
        "https://api.tarifftrust.com/v2/estimates",
    )
    assert request.headers["Authorization"] == "Bearer tarifftrust_test"
    assert request.headers["Content-Type"] == "application/json"
    assert request.headers["User-Agent"].startswith(f"tarifftrust-python/{tarifftrust.__version__}")
    assert api.sent == {"hts": "6109.10.00.12", "origin": "CN", "customs_value": "10000"}
    assert result.estimated_duty == "2400.00"


def test_decimals_and_dates_are_sent_as_the_api_reads_them(api, client):
    api.answer()
    client.estimate(
        hts="6109100012",
        origin="CN",
        customs_value=Decimal("10000.50"),
        as_of=date(2026, 4, 5),
        facts={"weight": Decimal("1.5")},
    )
    assert api.sent["customs_value"] == "10000.50"
    assert api.sent["as_of"] == "2026-04-05"
    assert api.sent["facts"] == {"weight": "1.5"}


def test_what_cannot_be_sent_is_said_before_the_request(api, client):
    with pytest.raises(TypeError, match="object cannot be sent"):
        client.estimate(hts="6109100012", origin="CN", customs_value=object())
    assert not api.requests


def test_a_reserved_word_is_an_argument_with_an_underscore(api, client):
    api.answer()
    client.estimate_history(
        hts="6109100012", origin="CN", from_=date(2025, 1, 1), through="2026-01-01"
    )
    assert api.sent["from"] == "2025-01-01" and api.sent["through"] == "2026-01-01"
    assert "from_" not in api.sent


def test_a_path_and_a_query_are_encoded(api, client):
    api.answer()
    client.get_hts("61/09")
    assert api.requests[0].url.raw_path == b"/v2/hts/61%2F09"
    api.answer()
    client.search_hts(q="cotton t-shirt", limit=5)
    assert dict(api.requests[1].url.params) == {"q": "cotton t-shirt", "limit": "5"}


def test_the_key_comes_from_the_environment(monkeypatch):
    monkeypatch.setenv("TARIFFTRUST_API_KEY", "tarifftrust_env")
    seen = []

    def handler(request):
        seen.append(request.headers["Authorization"])
        return httpx.Response(200, json={})

    TariffTrust(http_client=httpx.Client(transport=httpx.MockTransport(handler))).list_facts()
    assert seen == ["Bearer tarifftrust_env"]


def test_without_a_key_only_the_status_is_sent(monkeypatch):
    monkeypatch.delenv("TARIFFTRUST_API_KEY", raising=False)
    seen = []

    def handler(request):
        seen.append(request)
        return httpx.Response(200, json={"engine_version": "2.17"})

    keyless = TariffTrust(http_client=httpx.Client(transport=httpx.MockTransport(handler)))
    assert keyless.get_status().engine_version == "2.17"
    assert "Authorization" not in seen[0].headers
    with pytest.raises(AuthenticationError, match="No API key"):
        keyless.list_facts()
    assert len(seen) == 1


def test_the_base_url_is_yours_to_change(api):
    local = TariffTrust(
        "k",
        base_url="http://api.localhost:8000/",
        http_client=httpx.Client(transport=httpx.MockTransport(api)),
    )
    api.answer()
    local.list_facts()
    assert str(api.requests[0].url) == "http://api.localhost:8000/v2/facts"


def test_the_base_url_comes_from_the_environment(api, monkeypatch):
    monkeypatch.setenv("TARIFFTRUST_BASE_URL", "http://api.localhost:8000")
    local = TariffTrust("k", http_client=httpx.Client(transport=httpx.MockTransport(api)))
    api.answer()
    local.list_facts()
    assert str(api.requests[0].url) == "http://api.localhost:8000/v2/facts"


# ---------- Idempotency ----------


def test_a_retry_sends_the_key_of_the_first_attempt(api, client):
    api.answer(429, REFUSED, {"Retry-After": "3"})
    api.answer(body={"status": "calculated"})
    client.estimate(hts="6109100012", origin="CN")
    first, second = [request.headers["Idempotency-Key"] for request in api.requests]
    assert first == second and len(first) == 36
    assert api.waits == [3.0]


def test_each_call_has_its_own_key_unless_you_give_one(api, client):
    api.answer()
    api.answer()
    api.answer()
    client.estimate(hts="6109100012", origin="CN")
    client.estimate(hts="6109100012", origin="CN")
    client.estimate(hts="6109100012", origin="CN", idempotency_key="po-1042")
    keys = [request.headers["Idempotency-Key"] for request in api.requests]
    assert keys[0] != keys[1] and keys[2] == "po-1042"


def test_a_read_sends_no_idempotency_key(api, client):
    api.answer()
    client.list_agreements()
    assert "Idempotency-Key" not in api.requests[0].headers


@pytest.mark.parametrize(
    "call",
    [
        lambda client: client.estimate(hts="1", origin="CN"),
        lambda client: client.estimate_batch(items=[]),
        lambda client: client.estimate_entry(lines=[]),
        lambda client: client.estimate_history(hts="1", origin="CN"),
    ],
)
def test_every_counted_operation_takes_an_idempotency_key(api, client, call):
    api.answer()
    call(client)
    assert "Idempotency-Key" in api.requests[0].headers


# ---------- Retries ----------


def test_a_refusal_with_a_retry_after_is_tried_again_up_to_the_limit(api, client):
    for _ in range(3):
        api.answer(503, {"error": {"code": "data_unavailable"}}, {"Retry-After": "5"})
    with pytest.raises(ServiceUnavailableError) as raised:
        client.list_facts()
    assert len(api.requests) == 3 and api.waits == [5.0, 5.0]
    assert raised.value.retry_after == 5 and raised.value.code == "data_unavailable"


def test_a_refusal_without_a_retry_after_stays_refused(api, client):
    # The API gives none when trying again cannot help.
    api.answer(503, {"error": {"code": "data_unavailable", "message": "Not published"}})
    with pytest.raises(ServiceUnavailableError):
        client.list_facts()
    assert len(api.requests) == 1 and not api.waits


def test_a_wait_longer_than_the_limit_is_left_to_the_caller(api, client):
    api.answer(503, {"error": {"code": "data_unavailable"}}, {"Retry-After": "3600"})
    with pytest.raises(ServiceUnavailableError) as raised:
        client.list_facts()
    assert raised.value.retry_after == 3600
    assert len(api.requests) == 1 and not api.waits


@pytest.mark.parametrize("status", [502, 503, 504])
def test_a_gateway_error_is_tried_again(api, client, status):
    api.answer(status, text="<html>Bad gateway</html>")
    api.answer(body={"facts": []})
    assert client.list_facts().facts == []
    assert len(api.requests) == 2 and 0 < api.waits[0] <= 0.5


def test_a_refused_request_is_never_tried_again(api, client):
    api.answer(422, {"error": {"code": "invalid_input", "message": "No", "fields": ["origin"]}})
    with pytest.raises(InvalidInputError) as raised:
        client.estimate(hts="1", origin="??")
    assert raised.value.fields == ["origin"]
    assert len(api.requests) == 1


def test_a_connection_failure_is_tried_again_with_the_same_key(api, client):
    api.fail(httpx.ConnectError("refused"))
    api.answer(body={"status": "calculated"})
    assert client.estimate(hts="1", origin="CN").status == "calculated"
    first, second = [request.headers["Idempotency-Key"] for request in api.requests]
    assert first == second


def test_failures_to_reach_the_api_are_raised_after_the_retries(api, client):
    for _ in range(3):
        api.fail(httpx.ConnectError("refused"))
    with pytest.raises(APIConnectionError, match="could not be reached") as raised:
        client.list_facts()
    assert not isinstance(raised.value, APITimeoutError)
    assert len(api.requests) == 3
    for _ in range(3):
        api.fail(httpx.ReadTimeout("slow"))
    with pytest.raises(APITimeoutError, match="in time"):
        client.list_facts()


def test_no_retry_when_you_ask_for_none(api):
    client = TariffTrust(
        "k", max_retries=0, http_client=httpx.Client(transport=httpx.MockTransport(api))
    )
    api.answer(429, REFUSED, {"Retry-After": "1"})
    with pytest.raises(RateLimitError):
        client.list_facts()
    assert len(api.requests) == 1


# ---------- Errors ----------


@pytest.mark.parametrize(
    ("status", "kind"),
    [
        (400, InvalidInputError),
        (401, AuthenticationError),
        (402, AccessRequiredError),
        (403, PermissionDeniedError),
        (404, NotFoundError),
        (409, ConflictError),
        (413, PayloadTooLargeError),
        (422, InvalidInputError),
        (429, RateLimitError),
        (503, ServiceUnavailableError),
    ],
)
def test_each_status_of_the_contract_has_its_error(api, client, status, kind):
    api.answer(status, {"error": {"code": "some_code", "message": "Said"}, "request_id": "r-9"})
    with pytest.raises(kind) as raised:
        client.list_facts()
    error = raised.value
    assert isinstance(error, APIError) and isinstance(error, TariffTrustError)
    assert (error.status, error.code, error.message) == (status, "some_code", "Said")
    assert error.request_id == "r-9"
    assert str(error) == f"some_code: Said (HTTP {status}; request r-9)"


def test_the_version_is_the_packages():
    project = (ROOT / "python/pyproject.toml").read_text()
    assert f'version = "{tarifftrust.__version__}"' in project


def test_every_error_of_the_contract_is_covered():
    from tarifftrust._errors import BY_STATUS

    contract = json.loads((ROOT / "openapi.json").read_text())
    statuses = {
        int(status)
        for item in contract["paths"].values()
        for operation in item.values()
        for status in operation["responses"]
        if status != "200"
    }
    assert statuses <= BY_STATUS.keys()


def test_an_answer_that_is_not_the_apis_still_gives_an_error(api, client):
    api.answer(403, text="<html>Forbidden</html>", headers={"X-Request-ID": "r-2"})
    with pytest.raises(PermissionDeniedError) as raised:
        client.list_facts()
    assert raised.value.code is None and raised.value.message == "HTTP 403"
    assert raised.value.request_id == "r-2" and raised.value.body is None


def test_an_error_that_is_a_plain_string_is_read_too(api, client):
    api.answer(429, {"error": "Too many"}, {"Retry-After": "1"})
    api.answer(429, {"error": "Too many"}, {"Retry-After": "1"})
    api.answer(429, {"error": "Too many"}, {"Retry-After": "1"})
    with pytest.raises(RateLimitError):
        client.list_facts()


def test_a_success_that_is_not_json_is_an_error(api, client):
    api.answer(200, text="<html>")
    with pytest.raises(TariffTrustError, match="not JSON"):
        client.list_facts()


def test_an_unknown_status_is_an_api_error(api, client):
    api.answer(500, {"error": {"code": "internal", "message": "Oops"}})
    with pytest.raises(APIError) as raised:
        client.list_facts()
    assert raised.value.status == 500 and type(raised.value) is APIError


# ---------- Async ----------


def test_the_async_client_does_the_same(api, async_client):
    async def run():
        api.answer(429, REFUSED, {"Retry-After": "2"})
        api.answer(body={"status": "calculated", "estimated_duty": "1.00"})
        result = await async_client.estimate(hts="1", origin="CN", customs_value=Decimal("10"))
        assert result.estimated_duty == "1.00"
        api.answer(404, {"error": {"code": "not_found", "message": "No"}})
        with pytest.raises(NotFoundError):
            await async_client.get_hts("0000")
        api.fail(httpx.ConnectError("refused"))
        api.answer(body={"facts": []})
        assert (await async_client.list_facts()).facts == []
        await async_client.close()

    asyncio.run(run())
    first, second = [request.headers["Idempotency-Key"] for request in api.requests[:2]]
    assert first == second and api.waits[0] == 2.0
    assert json.loads(api.requests[0].content)["customs_value"] == "10"


def test_a_client_closes_only_what_it_opened():
    with TariffTrust("k") as own:
        pass
    assert own._http.is_closed
    shared = httpx.Client(
        transport=httpx.MockTransport(lambda request: httpx.Response(200, json={}))
    )
    with TariffTrust("k", http_client=shared) as client:
        client.list_facts()
    assert not shared.is_closed
    client.list_facts()


def test_an_async_client_closes_only_what_it_opened():
    async def run():
        async with AsyncTariffTrust("k") as own:
            pass
        assert own._http.is_closed
        shared = httpx.AsyncClient(
            transport=httpx.MockTransport(lambda r: httpx.Response(200, json={}))
        )
        async with AsyncTariffTrust("k", http_client=shared):
            pass
        assert not shared.is_closed
        await shared.aclose()

    asyncio.run(run())


def test_the_timeout_applies_to_your_own_client_too(api):
    client = TariffTrust(
        "k", timeout=7.5, http_client=httpx.Client(transport=httpx.MockTransport(api))
    )
    api.answer()
    client.list_facts()
    assert api.requests[0].extensions["timeout"]["read"] == 7.5


def test_a_stray_newline_in_the_key_is_dropped(api):
    client = TariffTrust(
        "tarifftrust_test\n", http_client=httpx.Client(transport=httpx.MockTransport(api))
    )
    api.answer()
    client.list_facts()
    assert api.requests[0].headers["Authorization"] == "Bearer tarifftrust_test"


def test_an_idempotency_key_that_cannot_be_a_header_is_said_before_the_request(api, client):
    with pytest.raises(ValueError, match="ASCII"):
        client.estimate(hts="1", origin="CN", idempotency_key="commande-é")
    assert not api.requests


def test_an_answer_that_cannot_be_decoded_is_a_failure_to_reach_the_api(api, client):
    for _ in range(3):
        api.fail(httpx.DecodingError("bad gzip"))
    with pytest.raises(APIConnectionError):
        client.list_facts()
    assert len(api.requests) == 3
