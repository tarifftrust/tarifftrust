// The US duty of a cart, from your e-commerce backend, with the API key kept on the server.
//
//   npm install tarifftrust
//   TARIFFTRUST_API_KEY=tarifftrust_... node server.mjs
//   curl -X POST localhost:3000/duties -d '{"lines":[{"sku":"TEE-001","quantity":10}]}'
import { createServer } from "node:http";

import { TariffTrust } from "tarifftrust";

// Your catalog's customs fields, on the server: never take them from the shopper. The customs value
// is the declared value of the goods, not the retail price.
const CATALOG = new Map([
  ["TEE-001", { hts: "6109.10.00.12", origin: "CN", unitCustomsValue: "4.50" }],
  ["TEE-002", { hts: "6109.10.00.12", origin: "VN", unitCustomsValue: "5.25" }],
]);

const client = new TariffTrust();

function customsLines(cartLines) {
  if (!Array.isArray(cartLines) || cartLines.length === 0) {
    throw new RangeError("lines is a list of { sku, quantity }");
  }
  return cartLines.map((line) => {
    const { sku, quantity } = line ?? {};
    const product = CATALOG.get(sku);
    if (!product || !Number.isInteger(quantity) || quantity < 1) {
      throw new RangeError(`Not a line of the catalog: ${sku}`);
    }
    return {
      reference: sku,
      hts: product.hts,
      origin: product.origin,
      customs_value: (Number(product.unitCustomsValue) * quantity).toFixed(2),
    };
  });
}

/** What the storefront may show: unknown stays null, never a duty of 0. */
export async function dutiesOfCart(cartLines) {
  const entry = await client.estimateEntry({ lines: customsLines(cartLines) });
  return {
    status: entry.status,
    duty: entry.estimated_duty,
    fees: entry.estimated_fees,
    publication_id: entry.data.publication_id,
    lines: entry.lines.map((line) => ({
      sku: line.reference,
      status: line.status,
      duty: line.estimated_duty,
    })),
  };
}

async function readJson(request) {
  const chunks = [];
  for await (const chunk of request) chunks.push(chunk);
  return JSON.parse(Buffer.concat(chunks).toString() || "{}");
}

async function answer(request) {
  if (request.method !== "POST" || request.url !== "/duties") {
    return [404, { error: "POST /duties" }];
  }
  try {
    const cart = await readJson(request);
    return [200, await dutiesOfCart(cart?.lines ?? [])];
  } catch (error) {
    if (error instanceof SyntaxError || error instanceof RangeError) {
      return [400, { error: error.message }];
    }
    // Refused or out of reach: the request id, if any, is what to quote to TariffTrust's support.
    console.error(String(error));
    return [502, { error: "Duties are not available right now" }];
  }
}

createServer(async (request, response) => {
  const [status, body] = await answer(request);
  response.writeHead(status, { "Content-Type": "application/json" });
  response.end(JSON.stringify(body));
}).listen(Number(process.env.PORT ?? 3000));
