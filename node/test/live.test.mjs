// Every operation against a running API, only when you ask: an estimate counts in its quota.
//   TARIFFTRUST_LIVE_URL=https://api.tarifftrust.com TARIFFTRUST_API_KEY=... node --test test/live.test.mjs
import assert from "node:assert/strict";
import { randomUUID } from "node:crypto";
import { test } from "node:test";

import { APIError, NotFoundError, TariffTrust } from "../dist/esm/index.js";

const baseUrl = process.env.TARIFFTRUST_LIVE_URL;
const options = { skip: !baseUrl };
const client = new TariffTrust({ baseUrl });
const product = { hts: "6109.10.00.12", origin: "CN", customs_value: "10000" };

test("status", options, async () => {
  assert.ok((await client.getStatus()).engine_version);
});

test("estimate", options, async () => {
  const result = await client.estimate(product);
  assert.ok(["calculated", "partial", "needs_information"].includes(result.status));
  assert.ok(Array.isArray(result.duties ?? []));
});

test("estimateBatch", options, async () => {
  const batch = await client.estimateBatch({ items: [product, { ...product, origin: "VN" }] });
  assert.deepEqual(batch.results.map((item) => item.index), [0, 1]);
});

test("estimateEntry", options, async () => {
  const entry = await client.estimateEntry({ lines: [{ ...product, reference: "PO-1" }] });
  assert.equal(entry.lines[0].reference, "PO-1");
});

test("estimateHistory", options, async () => {
  const { covered_from: from } = await client.getStatus();
  const history = await client.estimateHistory({ ...product, from });
  assert.ok(history.points.length > 0);
});

test("catalog", options, async () => {
  const found = await client.searchHts({ q: "cotton t-shirt", limit: 2 });
  assert.ok(found.results.length <= 2);
  assert.ok((await client.getHts("6109.10.00.12")).code);
  await assert.rejects(client.getHts("0000.00.00.00"), NotFoundError);
  assert.ok(Array.isArray((await client.listAgreements()).agreements));
  assert.ok(Array.isArray((await client.listFacts()).facts));
});

test("saved estimates", options, async () => {
  const saved = await client.estimate({ ...product, save: true, label: "SDK live test" });
  assert.equal((await client.getSavedEstimate(saved.saved_estimate_id)).label, "SDK live test");
  const declaration = await client.estimateEntry({ lines: [product], save: true });
  assert.ok(declaration.saved_estimate_id);
  assert.equal((await client.listSavedEstimates({ limit: 2 })).limit, 2);
});

test("an idempotency key replays the answer", options, async () => {
  const idempotencyKey = `sdk-live-${randomUUID()}`;
  const first = await client.estimate(product, { idempotencyKey });
  assert.deepEqual(await client.estimate(product, { idempotencyKey }), first);
  await assert.rejects(client.estimate({ ...product, origin: "VN" }, { idempotencyKey }), (error) => {
    assert.ok(error instanceof APIError);
    return error.status === 409;
  });
});

test("a refused field is named", options, async () => {
  await assert.rejects(client.estimate({ hts: "6109.10.00.12", origin: "NOT A COUNTRY" }), (error) => {
    assert.equal(error.status, 422);
    return error.fields.length > 0;
  });
});
