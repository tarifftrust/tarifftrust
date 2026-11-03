# TariffTrust: the US tariff API

Official Python and Node.js clients for the [TariffTrust API](https://tarifftrust.com/api/), with
examples. Send an HTS code, a country of origin and a value. Get every US import duty and fee that
applies, from the tariff schedule and Sections 301, 232, 201 and 338 to the entry fees, each with its
official, dated source.

Create your key in [your workspace](https://tarifftrust.com/keys/); your plan must include the API
([plans](https://tarifftrust.com/pricing/)). Keep the key on your server, never in a browser or a
mobile app.

## Python

Python 3.10 or later, sync and async.

```bash
pip install tarifftrust
```

```python
from tarifftrust import TariffTrust

client = TariffTrust(api_key="tarifftrust_...")  # or set TARIFFTRUST_API_KEY

result = client.estimate(hts="6109.10.00.12", origin="CN", customs_value="10000")

print(result.status, result.estimated_duty)
for component in result.components:
    print(component.label, component.amount, component.source.url)
```

Everything else is in the [Python client's guide](python/README.md).

## Node.js

Node.js 20 or later, TypeScript types included, no dependency.

```bash
npm install tarifftrust
```

```ts
import { TariffTrust } from "tarifftrust";

const client = new TariffTrust({ apiKey: "tarifftrust_..." }); // or set TARIFFTRUST_API_KEY

const result = await client.estimate({ hts: "6109.10.00.12", origin: "CN", customs_value: "10000" });

console.log(result.status, result.estimated_duty);
for (const component of result.components) {
  console.log(component.label, component.amount, component.source.url);
}
```

Everything else is in the [Node.js client's guide](node/README.md).

## What the clients do for you

- **Safe retries.** Each estimate carries an idempotency key. If the connection drops or the API asks
  to wait, the call is tried again with the same key, and it counts once in your quota.
- **Errors you can act on.** Each refusal is its own exception, with its code, the fields refused and
  the request id to quote to support.
- **Types from the contract.** Every request and answer field is typed and described, generated from
  the [OpenAPI contract](openapi.json). A daily check compares it with the one the API serves.

## Read the answer

Read `status` first, then the amounts. They are decimal strings in US dollars, so that nothing is
lost to floating point.

**Unknown is never zero.** When `estimated_duty` is `None` in Python or `null` in Node.js, the duty
could not be established: only `known_duty_subtotal` is. A question nobody answered is taken in its ordinary case and named in
`assumptions`, with what each other answer would change. See
[the guide](https://tarifftrust.com/guides/#answer).

For several products entered together, use `estimate_entry` in Python or `estimateEntry` in Node.js:
MPF and HMF are charged once on a declaration, so adding up single-product estimates gives a wrong
total.

## Examples

| Example | What it shows |
| --- | --- |
| [Landed cost in an ERP](examples/erp-landed-cost) | Python: a purchase order as one declaration, landed cost per unit |
| [E-commerce backend](examples/ecommerce-server) | Node.js: the duties of a cart, for Shopify, WooCommerce and others |
| [Next.js](examples/nextjs) | A form and a route handler, with the key on the server |
| [Google Sheets](examples/google-sheets) | `=TARIFFTRUST_DUTY("6109.10.00.12", "CN", 10000)` |
| [MCP](examples/mcp) | US tariffs as tools for Claude Code, Claude Desktop and Cursor |

## Operations

<!-- operations:start -->
| Python | Node.js | Route | What it does |
| --- | --- | --- | --- |
| `list_agreements` | `listAgreements` | [`GET /v1/agreements`](https://tarifftrust.com/api/reference/#list-agreements) | List the trade agreements |
| `estimate` | `estimate` | [`POST /v1/estimates`](https://tarifftrust.com/api/reference/#estimate) | Estimate one product |
| `estimate_batch` | `estimateBatch` | [`POST /v1/estimates/batch`](https://tarifftrust.com/api/reference/#estimate-batch) | Estimate up to 200 products |
| `estimate_entry` | `estimateEntry` | [`POST /v1/estimates/entry`](https://tarifftrust.com/api/reference/#estimate-entry) | Estimate a whole import declaration |
| `estimate_history` | `estimateHistory` | [`POST /v1/estimates/history`](https://tarifftrust.com/api/reference/#estimate-history) | Estimate one product at every change of the tariff |
| `list_facts` | `listFacts` | [`GET /v1/facts`](https://tarifftrust.com/api/reference/#list-facts) | List the questions an estimate may ask |
| `search_hts` | `searchHts` | [`GET /v1/hts`](https://tarifftrust.com/api/reference/#search-hts) | Search the US tariff schedule |
| `get_hts` | `getHts` | [`GET /v1/hts/{code}`](https://tarifftrust.com/api/reference/#get-hts) | Read one line of the US tariff schedule |
| `list_saved_estimates` | `listSavedEstimates` | [`GET /v1/saved-estimates`](https://tarifftrust.com/api/reference/#list-saved-estimates) | List the saved estimates |
| `save_estimate` | `saveEstimate` | [`POST /v1/saved-estimates`](https://tarifftrust.com/api/reference/#save-estimate) | Calculate and save an estimate |
| `get_saved_estimate` | `getSavedEstimate` | [`GET /v1/saved-estimates/{id}`](https://tarifftrust.com/api/reference/#get-saved-estimate) | Read a saved estimate |
| `get_status` | `getStatus` | [`GET /v1/status`](https://tarifftrust.com/api/reference/#get-status) | Read the status and the coverage of the data |
<!-- operations:end -->

## Documentation

- [API reference](https://tarifftrust.com/api/reference/): every operation and field
- [Integration guides](https://tarifftrust.com/guides/): quick start, answers, declarations, MCP
- [Errors and limits](https://tarifftrust.com/api/reference/#errors): statuses, rate limits, quota
- [Changelog](https://tarifftrust.com/changelog/): what changed in the data and in the API
- [Data status](https://tarifftrust.com/status/): when each official source was read

## Development

The types and the operations of both clients are generated from `openapi.json`:

```bash
python scripts/generate.py --sync   # copy the contract the API serves, and generate
python scripts/generate.py --check  # fail when a generated file is out of date
```

Test the Python client:

```bash
cd python && uv run pytest
```

Test the Node.js client:

```bash
cd node && npm install && npm test
```

Report a vulnerability to [security@tarifftrust.com](mailto:security@tarifftrust.com), and anything
else in [the issues](https://github.com/tarifftrust/tarifftrust/issues) or to
[support@tarifftrust.com](mailto:support@tarifftrust.com).

## License

The code here is under the [MIT license](LICENSE). The API itself is subject to the
[terms of service](https://tarifftrust.com/terms/).

TariffTrust provides informational estimates from official US sources. It is not a customs broker and
does not issue binding classifications or customs determinations.
