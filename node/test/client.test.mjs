// What each call sends, when it is tried again, and what it raises.
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { test } from "node:test";
import { inspect } from "node:util";

import {
  AccessRequiredError,
  APIConnectionError,
  APIError,
  APITimeoutError,
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
  VERSION,
} from "../dist/esm/index.js";

const json = (status, body, headers = {}) =>
  new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json", ...headers } });

/** A client whose requests are answered in order, and what it sent. */
function stubbed(answers, options = {}) {
  const requests = [];
  const client = new TariffTrust({
    apiKey: "tarifftrust_test",
    ...options,
    fetch: async (url, init) => {
      requests.push({ url, ...init });
      const answer = answers.shift();
      if (answer instanceof Error) throw answer;
      return answer;
    },
  });
  return { client, requests };
}

const refused = (status, code = "some_code", headers = {}) =>
  json(status, { error: { code, message: "Said" }, request_id: "r-9" }, headers);

test("a call sends the key and the fields as given", async () => {
  const { client, requests } = stubbed([json(200, { estimated_duty: "2400.00" })]);
  const result = await client.estimate({ hts: "6109.10.00.12", origin: "CN", customs_value: "10000" });
  const [request] = requests;
  assert.equal(request.url, "https://api.tarifftrust.com/v1/estimates");
  assert.equal(request.method, "POST");
  assert.equal(request.headers.Authorization, "Bearer tarifftrust_test");
  assert.equal(request.headers["Content-Type"], "application/json");
  assert.match(request.headers["User-Agent"], new RegExp(`^tarifftrust-node/${VERSION} node/`));
  assert.deepEqual(JSON.parse(request.body), { hts: "6109.10.00.12", origin: "CN", customs_value: "10000" });
  assert.equal(result.estimated_duty, "2400.00");
});

test("a path and a query are encoded, and what is unset is not sent", async () => {
  const { client, requests } = stubbed([json(200, {}), json(200, {}), json(200, {})]);
  await client.getHts("61/09");
  assert.equal(requests[0].url, "https://api.tarifftrust.com/v1/hts/61%2F09");
  assert.equal(requests[0].body, undefined);
  await client.searchHts({ q: "cotton t-shirt", limit: 5, chapter: undefined });
  assert.equal(requests[1].url, "https://api.tarifftrust.com/v1/hts?q=cotton+t-shirt&limit=5");
  await client.searchHts();
  assert.equal(requests[2].url, "https://api.tarifftrust.com/v1/hts");
});

test("the key comes from the environment", async () => {
  process.env.TARIFFTRUST_API_KEY = "tarifftrust_env";
  try {
    const seen = [];
    const client = new TariffTrust({
      fetch: async (_, init) => (seen.push(init.headers.Authorization), json(200, {})),
    });
    await client.listFacts();
    assert.deepEqual(seen, ["Bearer tarifftrust_env"]);
  } finally {
    delete process.env.TARIFFTRUST_API_KEY;
  }
});

test("without a key only the status is sent", async () => {
  const seen = [];
  const client = new TariffTrust({
    fetch: async (_, init) => (seen.push(init), json(200, { engine_version: "2.17" })),
  });
  assert.equal((await client.getStatus()).engine_version, "2.17");
  assert.equal(seen[0].headers.Authorization, undefined);
  await assert.rejects(client.listFacts(), AuthenticationError);
  assert.equal(seen.length, 1);
});

test("the base URL is yours to change", async () => {
  const { client, requests } = stubbed([json(200, {})], { baseUrl: "http://api.localhost:8000/" });
  await client.listFacts();
  assert.equal(requests[0].url, "http://api.localhost:8000/v1/facts");
});

test("the base URL comes from the environment", async () => {
  process.env.TARIFFTRUST_BASE_URL = "http://api.localhost:8000";
  try {
    const { client, requests } = stubbed([json(200, {})]);
    await client.listFacts();
    assert.equal(requests[0].url, "http://api.localhost:8000/v1/facts");
  } finally {
    delete process.env.TARIFFTRUST_BASE_URL;
  }
});

test("a retry sends the idempotency key of the first attempt", async () => {
  const { client, requests } = stubbed([
    refused(429, "rate_limited", { "Retry-After": "0" }),
    json(200, { status: "calculated" }),
  ]);
  await client.estimate({ hts: "1", origin: "CN" });
  const [first, second] = requests.map((request) => request.headers["Idempotency-Key"]);
  assert.equal(first, second);
  assert.equal(first.length, 36);
});

test("each call has its own idempotency key unless you give one", async () => {
  const { client, requests } = stubbed([json(200, {}), json(200, {}), json(200, {})]);
  await client.estimate({ hts: "1", origin: "CN" });
  await client.estimate({ hts: "1", origin: "CN" });
  await client.estimate({ hts: "1", origin: "CN" }, { idempotencyKey: "po-1042" });
  const keys = requests.map((request) => request.headers["Idempotency-Key"]);
  assert.notEqual(keys[0], keys[1]);
  assert.equal(keys[2], "po-1042");
});

test("every counted operation takes an idempotency key, and a read none", async () => {
  const { client, requests } = stubbed(Array.from({ length: 6 }, () => json(200, {})));
  await client.estimate({ hts: "1", origin: "CN" });
  await client.estimateBatch({ items: [] });
  await client.estimateEntry({ lines: [] });
  await client.estimateHistory({ hts: "1", origin: "CN" });
  await client.saveEstimate({ estimate: { hts: "1", origin: "CN" } });
  await client.listAgreements();
  assert.deepEqual(
    requests.map((request) => "Idempotency-Key" in request.headers),
    [true, true, true, true, true, false],
  );
});

test("a refusal with a retry-after is tried again up to the limit", async () => {
  const headers = { "Retry-After": "0" };
  const { client, requests } = stubbed([
    refused(503, "data_unavailable", headers),
    refused(503, "data_unavailable", headers),
    refused(503, "data_unavailable", headers),
  ]);
  await assert.rejects(client.listFacts(), (error) => {
    assert.ok(error instanceof ServiceUnavailableError);
    assert.equal(error.retryAfter, 0);
    assert.equal(error.code, "data_unavailable");
    return true;
  });
  assert.equal(requests.length, 3);
});

test("a refusal without a retry-after stays refused", async () => {
  const { client, requests } = stubbed([refused(503, "data_unavailable")]);
  await assert.rejects(client.listFacts(), ServiceUnavailableError);
  assert.equal(requests.length, 1);
});

test("a wait longer than the limit is left to the caller", async () => {
  const { client, requests } = stubbed([refused(503, "data_unavailable", { "Retry-After": "3600" })]);
  await assert.rejects(client.listFacts(), (error) => error.retryAfter === 3600);
  assert.equal(requests.length, 1);
});

for (const status of [502, 503, 504]) {
  test(`a gateway error ${status} is tried again`, async () => {
    const { client, requests } = stubbed([
      new Response("<html>Bad gateway</html>", { status }),
      json(200, { facts: [] }),
    ]);
    assert.deepEqual((await client.listFacts()).facts, []);
    assert.equal(requests.length, 2);
  });
}

test("a refused request is never tried again", async () => {
  const { client, requests } = stubbed([
    json(422, { error: { code: "invalid_input", message: "No", fields: ["origin"] } }),
  ]);
  await assert.rejects(client.estimate({ hts: "1", origin: "??" }), (error) => {
    assert.ok(error instanceof InvalidInputError);
    assert.deepEqual(error.fields, ["origin"]);
    return true;
  });
  assert.equal(requests.length, 1);
});

test("a connection failure is tried again with the same key", async () => {
  const { client, requests } = stubbed([new TypeError("fetch failed"), json(200, { status: "calculated" })]);
  assert.equal((await client.estimate({ hts: "1", origin: "CN" })).status, "calculated");
  assert.equal(requests[0].headers["Idempotency-Key"], requests[1].headers["Idempotency-Key"]);
});

test("failures to reach the API are raised after the retries", async () => {
  const failure = new TypeError("fetch failed");
  const { client, requests } = stubbed([failure, failure, failure]);
  await assert.rejects(client.listFacts(), (error) => {
    assert.ok(error instanceof APIConnectionError);
    assert.ok(!(error instanceof APITimeoutError));
    assert.equal(error.cause, failure);
    return true;
  });
  assert.equal(requests.length, 3);
});

test("a timeout is said as such", async () => {
  const client = new TariffTrust({
    apiKey: "k",
    timeoutMs: 5,
    maxRetries: 0,
    fetch: (_, init) =>
      new Promise((_, reject) => {
        // A real request's socket keeps the process alive: the timeout's timer does not.
        const alive = setInterval(() => {}, 1);
        init.signal.addEventListener("abort", () => {
          clearInterval(alive);
          reject(init.signal.reason);
        });
      }),
  });
  await assert.rejects(client.listFacts(), APITimeoutError);
});

test("a call you cancel is not tried again", async () => {
  const controller = new AbortController();
  let calls = 0;
  const client = new TariffTrust({
    apiKey: "k",
    fetch: (_, init) =>
      new Promise((_, reject) => {
        calls += 1;
        init.signal.addEventListener("abort", () => reject(init.signal.reason));
        controller.abort(new Error("Cancelled"));
      }),
  });
  await assert.rejects(client.listFacts({ signal: controller.signal }), /Cancelled/);
  assert.equal(calls, 1);
});

test("no retry when you ask for none", async () => {
  const { client, requests } = stubbed([refused(429, "rate_limited", { "Retry-After": "1" })], { maxRetries: 0 });
  await assert.rejects(client.listFacts(), RateLimitError);
  assert.equal(requests.length, 1);
});

const statuses = [
  [400, InvalidInputError],
  [401, AuthenticationError],
  [402, AccessRequiredError],
  [403, PermissionDeniedError],
  [404, NotFoundError],
  [409, ConflictError],
  [413, PayloadTooLargeError],
  [422, InvalidInputError],
  [429, RateLimitError],
  [503, ServiceUnavailableError],
];

for (const [status, Kind] of statuses) {
  test(`status ${status} has its error`, async () => {
    const { client } = stubbed([refused(status)]);
    await assert.rejects(client.listFacts(), (error) => {
      assert.ok(error instanceof Kind && error instanceof APIError && error instanceof TariffTrustError);
      assert.equal(error.name, Kind.name);
      assert.equal(error.status, status);
      assert.equal(error.code, "some_code");
      assert.equal(error.requestId, "r-9");
      assert.equal(error.message, "Said");
      assert.equal(String(error), `some_code: Said (HTTP ${status}; request r-9)`);
      return true;
    });
  });
}

test("every error of the contract is covered", () => {
  const contract = JSON.parse(readFileSync(new URL("../../openapi.json", import.meta.url)));
  const known = new Set(statuses.map(([status]) => status));
  for (const item of Object.values(contract.paths)) {
    for (const operation of Object.values(item)) {
      for (const status of Object.keys(operation.responses)) {
        if (status !== "200") assert.ok(known.has(Number(status)), status);
      }
    }
  }
});

test("an answer that is not the API's still gives an error", async () => {
  const { client } = stubbed([
    new Response("<html>Forbidden</html>", { status: 403, headers: { "X-Request-ID": "r-2" } }),
  ]);
  await assert.rejects(client.listFacts(), (error) => {
    assert.ok(error instanceof PermissionDeniedError);
    assert.equal(error.code, null);
    assert.equal(error.requestId, "r-2");
    assert.equal(error.body, null);
    return true;
  });
});

test("an error that is a plain string is read too", async () => {
  const { client } = stubbed([json(403, { error: "Forbidden" })]);
  await assert.rejects(client.listFacts(), PermissionDeniedError);
});

test("a success that is not JSON is an error", async () => {
  const { client } = stubbed([new Response("<html>", { status: 200 })]);
  await assert.rejects(client.listFacts(), (error) => {
    assert.ok(error instanceof TariffTrustError && !(error instanceof APIConnectionError));
    assert.match(error.message, /not JSON/);
    return true;
  });
});

test("logging a client never prints its key", () => {
  const client = new TariffTrust({ apiKey: "tarifftrust_secret" });
  assert.doesNotMatch(inspect(client, { depth: 5, showHidden: true }), /tarifftrust_secret/);
  assert.doesNotMatch(JSON.stringify(client), /tarifftrust_secret/);
});

test("a stray newline in the key is dropped", async () => {
  const { client, requests } = stubbed([json(200, {})], { apiKey: "tarifftrust_test\n" });
  await client.listFacts();
  assert.equal(requests[0].headers.Authorization, "Bearer tarifftrust_test");
});

test("fetch is called as a plain function", async () => {
  let receiver = "unset";
  const client = new TariffTrust({
    apiKey: "k",
    fetch: function () {
      receiver = this;
      return Promise.resolve(json(200, {}));
    },
  });
  await client.listFacts();
  assert.equal(receiver, undefined);
});

test("a redirect is reported, not followed", async () => {
  const { client, requests } = stubbed([new Response(null, { status: 301 })]);
  await assert.rejects(client.listFacts(), (error) => error instanceof APIError && error.status === 301);
  assert.equal(requests[0].redirect, "manual");
});

test("an empty idempotency key or base URL counts as none", async () => {
  process.env.TARIFFTRUST_BASE_URL = "";
  try {
    const { client, requests } = stubbed([json(200, {})]);
    await client.estimate({ hts: "1", origin: "CN" }, { idempotencyKey: "" });
    assert.equal(requests[0].headers["Idempotency-Key"].length, 36);
    assert.match(requests[0].url, /^https:\/\/api\.tarifftrust\.com\//);
  } finally {
    delete process.env.TARIFFTRUST_BASE_URL;
  }
});

test("an idempotency key that cannot be a header is said before the request", async () => {
  const { client, requests } = stubbed([]);
  await assert.rejects(client.estimate({ hts: "1", origin: "CN" }, { idempotencyKey: "commande-é" }), RangeError);
  assert.equal(requests.length, 0);
});

test("every operation of the contract is a method", () => {
  const contract = JSON.parse(readFileSync(new URL("../../openapi.json", import.meta.url)));
  const client = new TariffTrust({ apiKey: "k" });
  for (const item of Object.values(contract.paths)) {
    for (const operation of Object.values(item)) {
      const camel = operation.operationId.replace(/_(.)/g, (_, letter) => letter.toUpperCase());
      assert.equal(typeof client[camel], "function", camel);
    }
  }
});

test("the version is the package's", () => {
  const manifest = JSON.parse(readFileSync(new URL("../package.json", import.meta.url)));
  assert.equal(VERSION, manifest.version);
});
