// The package works from require() too, with the same errors.
const assert = require("node:assert/strict");
const { test } = require("node:test");

const { TariffTrust, NotFoundError } = require("../dist/cjs/index.js");

test("require gives the client", async () => {
  const client = new TariffTrust({
    apiKey: "k",
    fetch: async () =>
      new Response(JSON.stringify({ error: { code: "not_found", message: "No" } }), { status: 404 }),
  });
  await assert.rejects(client.getHts("0000"), NotFoundError);
});
