// Compiled, never run: what a TypeScript user writes type-checks, and what is wrong does not.
import { TariffTrust } from "../dist/esm/index.js";
import type { BatchFailure, BatchSuccess, Declaration, Estimate } from "../dist/esm/index.js";

const client = new TariffTrust({ apiKey: "k" });

export async function usage(): Promise<void> {
  const result: Estimate = await client.estimate({
    hts: "6109.10.00.12",
    origin: "CN",
    customs_value: "10000",
    transport_mode: "ocean",
    facts: { weight: 1.5 },
  });
  const duty: string | null | undefined = result.estimated_duty;
  const amount: string | null | undefined = result.duties?.[0]?.amount;
  console.log(duty, amount, result.status === "calculated");

  const batch = await client.estimateBatch({ items: [{ hts: "1", origin: "CN" }] });
  for (const item of batch.results) {
    if ("result" in item) console.log((item satisfies BatchSuccess).result.status);
    else console.log((item satisfies BatchFailure).error.code);
  }

  const entry: Declaration = await client.estimateEntry(
    { lines: [{ hts: "1", origin: "CN", reference: "PO-1" }], transport_mode: "air" },
    { idempotencyKey: "po-1", timeoutMs: 1000 },
  );
  console.log(entry.lines[0]?.status);

  await client.estimateHistory({ hts: "1", origin: "CN", from: "2025-01-01" });
  await client.estimate({ hts: "1", origin: "CN", save: true, label: "x" });
  await client.estimateEntry({ lines: [], save: true });
  (await client.searchHts({ q: "cotton", limit: 5 })).results[0]?.code;
  (await client.searchHts()).count;
  (await client.getHts("6109.10.00.12")).general;
  (await client.listSavedEstimates({ limit: 2 })).results[0]?.id;
  (await client.getSavedEstimate("id")).label;
  (await client.getStatus()).engine_version;
  (await client.listAgreements()).agreements[0]?.symbol;
  (await client.listFacts()).facts[0]?.name;
  (await client.estimateHistory({ hts: "1", origin: "CN" })).covered_windows[0]?.from;

  // @ts-expect-error origin is required.
  await client.estimate({ hts: "1" });
  // @ts-expect-error not a transport mode.
  await client.estimate({ hts: "1", origin: "CN", transport_mode: "rail" });
  // @ts-expect-error not a field of the answer.
  console.log(result.estimated_dutty);
}
