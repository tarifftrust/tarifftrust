# tarifftrust: US tariff API client for Node.js and TypeScript

The official Node.js and TypeScript client for the [TariffTrust API](https://tarifftrust.com/api/).
Send an HTS code, a country of origin and a value. Get every US import duty and fee that applies, from
the tariff schedule and Sections 301, 232, 201 and 338 to the entry fees, each with its official, dated
source.

```bash
npm install tarifftrust
```

Requires Node.js 20 or later. No dependency, TypeScript types included, ESM and CommonJS. For server
use: your API key must never reach a browser.

## Quick start

Create a key in [your workspace](https://tarifftrust.com/keys/); your plan must include the API
([plans](https://tarifftrust.com/pricing/)).

```ts
import { TariffTrust } from "tarifftrust";

const client = new TariffTrust({ apiKey: "tarifftrust_..." }); // or set TARIFFTRUST_API_KEY

const result = await client.estimate({ hts: "6109.10.00.12", origin: "CN", customs_value: "10000" });

console.log(result.status, result.estimated_duty);
for (const component of result.components) {
  console.log(component.label, component.amount, component.source.url);
}
```

Read `status` first, then the amounts: decimal strings in US dollars. The fields keep their names in
the API, as you see them in the [reference](https://tarifftrust.com/api/reference/). An answer is the
API's JSON: a list it leaves out is `undefined`, so read `result.assumptions ?? []`.

**Unknown is never zero.** When `estimated_duty` is `null`, the duty could not be established: only
`known_duty_subtotal` is. See [the guide](https://tarifftrust.com/guides/#answer).

## A whole declaration

MPF and HMF are charged once on a declaration: adding up single-product estimates gives a wrong total.

```ts
const entry = await client.estimateEntry({
  transport_mode: "ocean",
  lines: [
    { reference: "PO-1042-1", hts: "6109.10.00.12", origin: "CN", customs_value: "1000" },
    { reference: "PO-1042-2", hts: "6109.10.00.12", origin: "VN", customs_value: "2500" },
  ],
});
console.log(entry.estimated_duty, entry.total_fees, entry.estimated_landed_cost);
```

## Several products, a history, a saved estimate

```ts
const batch = await client.estimateBatch({
  items: [
    { hts: "6109.10.00.12", origin: "CN", customs_value: "10000" },
    { hts: "6109.10.00.12", origin: "VN", customs_value: "10000" },
  ],
});
for (const item of batch.results) {
  console.log(item.index, "result" in item ? item.result.estimated_duty : item.error.code);
}

const history = await client.estimateHistory({
  hts: "6109.10.00.12",
  origin: "CN",
  customs_value: "10000",
  from: "2026-10-01",
});
for (const point of history.points) console.log(point.as_of, point.estimated_duty);

const saved = await client.saveEstimate({
  estimate: { hts: "6109.10.00.12", origin: "CN", customs_value: "10000" },
});
console.log(saved.id);
```

## The catalog

```ts
const found = await client.searchHts({ q: "cotton t-shirt", limit: 5 });
const line = await client.getHts("6109.10.00.12");
console.log(line.description, line.general);
```

## Errors

Each refusal of the API is its own class, under `APIError`.

```ts
import { APIError, InvalidInputError } from "tarifftrust";

try {
  await client.estimate({ hts: "6109.10.00.12", origin: "??", customs_value: "10000" });
} catch (error) {
  if (error instanceof InvalidInputError) {
    console.log(error.fields); // each field refused
  } else if (error instanceof APIError) {
    console.log(error.status, error.code, error.message, error.requestId);
  } else {
    throw error;
  }
}
```

| Class | Status | When |
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

All of them extend `TariffTrustError`.

## Retries and idempotency

A call is tried again, twice by default, after a connection failure, a timeout or a gateway error, or
when the API gives a `Retry-After` of 60 seconds or less. A refusal without one is raised at once:
trying again would not help.

Every estimate carries an idempotency key, the same on each attempt, so a retry counts once in your
quota. To make a retry of your own safe, across restarts for instance, give your own key:

```ts
await client.estimate(
  { hts: "6109.10.00.12", origin: "CN", customs_value: "10000" },
  { idempotencyKey: "po-1042" },
);
```

Within 7 days, the same key with the same request gives the first response, counted once; with another
request, a `ConflictError`.

## Settings

```ts
const client = new TariffTrust({
  apiKey: "tarifftrust_...", // or TARIFFTRUST_API_KEY
  timeoutMs: 60_000, // for a whole attempt
  maxRetries: 2,
  maxRetryWaitSeconds: 60, // the longest Retry-After waited for
  fetch: globalThis.fetch, // your own fetch: a proxy, your certificates
});
```

Each call also takes `{ signal, timeoutMs }` as its last argument.

## Operations

<!-- operations:start -->
| Method | Route | What it does |
| --- | --- | --- |
| `client.listAgreements()` | [`GET /v1/agreements`](https://tarifftrust.com/api/reference/#list-agreements) | List the trade agreements |
| `client.estimate()` | [`POST /v1/estimates`](https://tarifftrust.com/api/reference/#estimate) | Estimate one product |
| `client.estimateBatch()` | [`POST /v1/estimates/batch`](https://tarifftrust.com/api/reference/#estimate-batch) | Estimate up to 200 products |
| `client.estimateEntry()` | [`POST /v1/estimates/entry`](https://tarifftrust.com/api/reference/#estimate-entry) | Estimate a whole import declaration |
| `client.estimateHistory()` | [`POST /v1/estimates/history`](https://tarifftrust.com/api/reference/#estimate-history) | Estimate one product at every change of the tariff |
| `client.listFacts()` | [`GET /v1/facts`](https://tarifftrust.com/api/reference/#list-facts) | List the questions an estimate may ask |
| `client.searchHts()` | [`GET /v1/hts`](https://tarifftrust.com/api/reference/#search-hts) | Search the US tariff schedule |
| `client.getHts()` | [`GET /v1/hts/{code}`](https://tarifftrust.com/api/reference/#get-hts) | Read one line of the US tariff schedule |
| `client.listSavedEstimates()` | [`GET /v1/saved-estimates`](https://tarifftrust.com/api/reference/#list-saved-estimates) | List the saved estimates |
| `client.saveEstimate()` | [`POST /v1/saved-estimates`](https://tarifftrust.com/api/reference/#save-estimate) | Calculate and save an estimate |
| `client.getSavedEstimate()` | [`GET /v1/saved-estimates/{id}`](https://tarifftrust.com/api/reference/#get-saved-estimate) | Read a saved estimate |
| `client.getStatus()` | [`GET /v1/status`](https://tarifftrust.com/api/reference/#get-status) | Read the status and the coverage of the data |
<!-- operations:end -->

## Links

[API reference](https://tarifftrust.com/api/reference/) ·
[Integration guides](https://tarifftrust.com/guides/) ·
[Examples](https://github.com/tarifftrust/tarifftrust/tree/main/examples) ·
[Changelog](https://tarifftrust.com/changelog/) ·
[Data status](https://tarifftrust.com/status/)

TariffTrust provides informational estimates from official US sources. It is not a customs broker and
does not issue binding classifications or customs determinations.
