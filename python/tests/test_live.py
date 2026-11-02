"""Every operation against a running API, only when you ask: an estimate counts in its quota.

TARIFFTRUST_LIVE_URL=https://api.tarifftrust.com TARIFFTRUST_API_KEY=... pytest tests/test_live.py
"""

import asyncio
import os

import pytest

from tarifftrust import APIError, AsyncTariffTrust, NotFoundError, TariffTrust, types

URL = os.environ.get("TARIFFTRUST_LIVE_URL")
pytestmark = pytest.mark.skipif(not URL, reason="TARIFFTRUST_LIVE_URL is not set")
PRODUCT = {"hts": "6109.10.00.12", "origin": "CN", "customs_value": "10000"}


def first_published_day(client):
    """The first day the API holds, for a history that does not leave its data."""
    starts = [item["valid_from"] for item in client.get_status().publications]
    return min(starts)


def read_all(value):
    """Read every declared field of an object and of the objects in it; the contract's required
    fields are there, as the TypeScript types promise."""
    if isinstance(value, types.Model):
        missing = value._required - value.to_dict().keys()
        assert not missing, f"{type(value).__name__} lacks {sorted(missing)}"
        for field in value._fields:
            read_all(getattr(value, field if field != "from" else "from_"))
    elif isinstance(value, list):
        for item in value:
            read_all(item)
    elif isinstance(value, dict):
        for item in value.values():
            read_all(item)


@pytest.fixture(scope="module")
def client():
    with TariffTrust(base_url=URL) as found:
        yield found


def test_status(client):
    status = client.get_status()
    assert status.engine_version
    read_all(status)


def test_estimate(client):
    result = client.estimate(**PRODUCT)
    assert isinstance(result, types.CalculationResult)
    assert result.status in {"calculated", "partial", "needs_information"}
    assert all(isinstance(item, types.Component) for item in result.components)
    read_all(result)


def test_estimate_batch(client):
    batch = client.estimate_batch(
        items=[
            PRODUCT,
            {**PRODUCT, "origin": "VN"},
        ]
    )
    assert [item.index for item in batch.results] == [0, 1]
    assert all(isinstance(item, (types.BatchSuccess, types.BatchFailure)) for item in batch.results)
    read_all(batch)


def test_estimate_entry(client):
    entry = client.estimate_entry(lines=[{**PRODUCT, "customs_value": "1000", "reference": "PO-1"}])
    assert isinstance(entry, types.EntryResult) and entry.lines[0].reference == "PO-1"
    read_all(entry)


def test_estimate_history(client):
    history = client.estimate_history(**PRODUCT, from_=first_published_day(client))
    assert isinstance(history.points[0], types.CalculationResult)
    read_all(history)


def test_catalog(client):
    found = client.search_hts(q="cotton t-shirt", limit=2)
    assert len(found.results) <= 2
    read_all(found)
    read_all(client.get_hts("6109.10.00.12"))
    with pytest.raises(NotFoundError):
        client.get_hts("0000.00.00.00")
    read_all(client.list_agreements())
    read_all(client.list_facts())


def test_saved_estimates(client):
    saved = client.save_estimate(estimate=PRODUCT, label="SDK live test")
    assert isinstance(saved.result, types.CalculationResult)
    read_all(saved)
    detail = client.get_saved_estimate(saved.id)
    assert detail.label == "SDK live test"
    read_all(detail)
    declaration = client.save_estimate(entry={"lines": [PRODUCT]})
    assert isinstance(declaration.result, types.EntryResult) and declaration.entry_id
    listed = client.list_saved_estimates(limit=2)
    assert listed.results and listed.limit == 2
    read_all(listed)


def test_an_idempotency_key_replays_the_answer(client):
    key = f"sdk-live-{os.urandom(8).hex()}"
    first = client.estimate(**PRODUCT, idempotency_key=key)
    second = client.estimate(**PRODUCT, idempotency_key=key)
    assert first == second
    with pytest.raises(APIError) as raised:
        client.estimate(**{**PRODUCT, "origin": "VN"}, idempotency_key=key)
    assert raised.value.status == 409


def test_a_refused_field_is_named(client):
    with pytest.raises(APIError) as raised:
        client.estimate(hts="6109.10.00.12", origin="NOT A COUNTRY", customs_value="1")
    assert raised.value.status == 422 and raised.value.fields


def test_async(client):
    async def run():
        async with AsyncTariffTrust(base_url=URL) as asynchronous:
            return await asynchronous.estimate(**PRODUCT)

    assert asyncio.run(run()).status
