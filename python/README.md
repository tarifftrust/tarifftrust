# tarifftrust: US tariff API client for Python

The official Python client for the [TariffTrust API](https://tarifftrust.com/api/). Send an HTS code,
a country of origin and a value. Get every US import duty and fee that applies, from the tariff
schedule and Sections 301, 232, 201 and 338 to the entry fees, each with its official source.

```bash
pip install tarifftrust
```

Requires Python 3.10 or later. Fully typed, sync and async.

## Quick start

Create a key in [your workspace](https://tarifftrust.com/keys/); your plan must include the API
([plans](https://tarifftrust.com/pricing/)). Keep it on your server.

```python
from tarifftrust import TariffTrust

client = TariffTrust(api_key="tarifftrust_...")  # or set TARIFFTRUST_API_KEY

result = client.estimate(hts="6109.10.00.12", origin="CN", customs_value="10000")

print(result.status, result.estimated_duty)
for duty in result.duties or []:
    print(duty.name, duty.rate, duty.amount, duty.source.url)
```

Read `status` first, then the amounts: decimal strings in US dollars, ready for `Decimal`.

**Unknown is never zero.** When `estimated_duty` is `None`, the duty is not established: with
`needs_information`, `missing` says what to send again; with `partial`, `withheld` says what is left
out for now. See [the guide](https://tarifftrust.com/guides/#answer).

## A whole declaration

MPF and HMF are charged once on a declaration: adding up single-product estimates gives a wrong total.

```python
entry = client.estimate_entry(
    transport_mode="ocean",
    lines=[
        {"reference": "PO-1042-1", "hts": "6109.10.00.12", "origin": "CN", "customs_value": "1000"},
        {"reference": "PO-1042-2", "hts": "6109.10.00.12", "origin": "VN", "customs_value": "2500"},
    ],
)
print(entry.estimated_duty, entry.estimated_fees, entry.estimated_landed_cost)
```

## Several products, a history, a saved estimate

```python
batch = client.estimate_batch(
    items=[
        {"hts": "6109.10.00.12", "origin": "CN", "customs_value": "10000"},
        {"hts": "6109.10.00.12", "origin": "VN", "customs_value": "10000"},
    ]
)
for item in batch.results:
    print(item.index, item.result.estimated_duty if hasattr(item, "result") else item.error.code)

history = client.estimate_history(
    hts="6109.10.00.12", origin="CN", customs_value="10000", from_="2026-10-01"
)
for point in history.points:
    print(point.as_of, point.estimated_duty)

saved = client.estimate(hts="6109.10.00.12", origin="CN", customs_value="10000", save=True)
print(client.get_saved_estimate(saved.saved_estimate_id).result.audit)
```

Send `save` on an estimate, an item of a batch or a declaration: the answer gives its
`saved_estimate_id`, and reading it gives the detail behind the answer in `audit`.

`from` is a reserved word in Python: it is `from_` here, as an argument and on an answer.

## The catalog

```python
found = client.search_hts(q="cotton t-shirt", limit=5)
line = client.get_hts("6109.10.00.12")
print(line.description, line.general)
```

## Async

`AsyncTariffTrust` has the same methods, awaited.

```python
import asyncio
from tarifftrust import AsyncTariffTrust


async def main():
    async with AsyncTariffTrust() as client:
        return await asyncio.gather(
            client.estimate(hts="6109.10.00.12", origin="CN", customs_value="10000"),
            client.estimate(hts="6109.10.00.12", origin="VN", customs_value="10000"),
        )
```

## Errors

Each refusal of the API is its own exception, under `APIError`.

```python
from tarifftrust import APIError, InvalidInputError, RateLimitError

try:
    result = client.estimate(hts="6109.10.00.12", origin="??", customs_value="10000")
except InvalidInputError as error:
    print(error.fields)  # each field refused
except APIError as error:
    print(error.status, error.code, error.message, error.request_id)
```

| Exception | Status | When |
| --- | --- | --- |
| `AuthenticationError` | 401 | No valid API key |
| `AccessRequiredError` | 402 | No active subscription, or the quota is used up (`quota_exceeded`) |
| `PermissionDeniedError` | 403 | The key lacks the permission, or the plan the API |
| `NotFoundError` | 404 | Nothing of that name |
| `ConflictError` | 409 | An idempotency key sent again with another request |
| `PayloadTooLargeError` | 413 | Send fewer products or lines |
| `InvalidInputError` | 400, 422 | `fields` names each field refused; a 400 is a body that is not valid JSON |
| `RateLimitError` | 429 | Too many requests |
| `ServiceUnavailableError` | 502, 503, 504 | Unavailable for now |
| `APIConnectionError`, `APITimeoutError` | | The API could not be reached |

All of them inherit from `TariffTrustError`.

## Retries and idempotency

A call is tried again, twice by default, after a connection failure, a timeout or a gateway error, or
when the API gives a `Retry-After` of 60 seconds or less. A refusal without one is raised at once:
trying again would not help.

Every estimate carries an idempotency key, the same on each attempt, so a retry counts once in your
quota. To make a retry of your own safe, across restarts for instance, give your own key:

```python
client.estimate(hts="6109.10.00.12", origin="CN", customs_value="10000", idempotency_key="po-1042")
```

Within 7 days, the same key with the same request gives the first response, counted once; with
another request, a `ConflictError`.

## Settings

```python
client = TariffTrust(
    api_key="tarifftrust_...",  # or TARIFFTRUST_API_KEY
    timeout=60.0,  # seconds, at each step of an attempt: connecting, sending, each read
    max_retries=2,
    max_retry_wait=60.0,  # the longest Retry-After waited for, in seconds
    http_client=None,  # your own httpx.Client (a proxy, your certificates): yours to close
)
```

## The answers

An answer is an object with the fields of the [reference](https://tarifftrust.com/api/reference/objects/)
as attributes, typed for your editor. A field the answer leaves out reads as its default or `None`. A
field newer than your version of the package reads as an attribute too. `to_dict()` gives the object
as the API sent it, and the types are in `tarifftrust.types`.

## Operations

<!-- operations:start -->
| Method | Route | What it does |
| --- | --- | --- |
| `client.list_agreements()` | [`GET /v2/agreements`](https://tarifftrust.com/api/reference/#list-agreements) | List the trade agreements |
| `client.estimate()` | [`POST /v2/estimates`](https://tarifftrust.com/api/reference/#estimate) | Estimate one product |
| `client.estimate_batch()` | [`POST /v2/estimates/batch`](https://tarifftrust.com/api/reference/#estimate-batch) | Estimate up to 200 products |
| `client.estimate_entry()` | [`POST /v2/estimates/entry`](https://tarifftrust.com/api/reference/#estimate-entry) | Estimate a whole import declaration |
| `client.estimate_history()` | [`POST /v2/estimates/history`](https://tarifftrust.com/api/reference/#estimate-history) | Estimate one product at every change of the tariff |
| `client.list_facts()` | [`GET /v2/facts`](https://tarifftrust.com/api/reference/#list-facts) | List the questions an estimate may ask |
| `client.search_hts()` | [`GET /v2/hts`](https://tarifftrust.com/api/reference/#search-hts) | Search the US tariff schedule |
| `client.get_hts()` | [`GET /v2/hts/{code}`](https://tarifftrust.com/api/reference/#get-hts) | Read one line of the US tariff schedule |
| `client.list_saved_estimates()` | [`GET /v2/saved-estimates`](https://tarifftrust.com/api/reference/#list-saved-estimates) | List the saved estimates |
| `client.get_saved_estimate()` | [`GET /v2/saved-estimates/{id}`](https://tarifftrust.com/api/reference/#get-saved-estimate) | Read a saved estimate |
| `client.get_status()` | [`GET /v2/status`](https://tarifftrust.com/api/reference/#get-status) | Read the status of the data |
<!-- operations:end -->

## Links

[API reference](https://tarifftrust.com/api/reference/) ·
[Integration guides](https://tarifftrust.com/guides/) ·
[Examples](https://github.com/tarifftrust/tarifftrust/tree/main/examples) ·
[Changelog](https://tarifftrust.com/changelog/) ·
[Data status](https://tarifftrust.com/status/)

TariffTrust provides informational estimates from official US sources. It is not a customs broker and
does not issue binding classifications or customs determinations.
