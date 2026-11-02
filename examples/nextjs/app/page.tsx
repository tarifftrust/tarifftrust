"use client";

import { type FormEvent, useState } from "react";

interface Answer {
  status?: string;
  duty?: string | null;
  known_subtotal?: string | null;
  lines?: { label: string; amount: string | null }[];
  error?: string;
}

export default function Page() {
  const [answer, setAnswer] = useState<Answer | null>(null);

  async function estimate(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const response = await fetch("/api/duty", {
      method: "POST",
      body: JSON.stringify(Object.fromEntries(new FormData(event.currentTarget))),
    });
    setAnswer(await response.json());
  }

  return (
    <main>
      <h1>US import duty</h1>
      <form onSubmit={estimate}>
        <input name="hts" defaultValue="6109.10.00.12" aria-label="HTS code" />
        <input name="origin" defaultValue="CN" aria-label="Country of origin" />
        <input name="customs_value" defaultValue="10000" aria-label="Customs value in USD" />
        <button>Estimate</button>
      </form>
      {answer?.error && <p>{answer.error}</p>}
      {answer?.status && (
        <>
          <p>
            {/* Unknown is never zero: without a duty, only the subtotal is established. */}
            {answer.duty != null
              ? `Estimated duty: $${answer.duty}`
              : `Duty unknown (${answer.status}). Established so far: ${answer.known_subtotal ?? "nothing"}`}
          </p>
          <ul>
            {answer.lines?.map(({ label, amount }) => (
              <li key={label}>
                {label}: {amount === null ? "unknown" : `$${amount}`}
              </li>
            ))}
          </ul>
        </>
      )}
    </main>
  );
}
