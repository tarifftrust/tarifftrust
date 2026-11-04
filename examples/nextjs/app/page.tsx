"use client";

import { type FormEvent, useState } from "react";

interface Answer {
  status?: string;
  duty?: string | null;
  lines?: { name: string; amount: string | null }[];
  missing?: string[];
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
            {/* Unknown is never zero: without a duty, the answer says what is missing. */}
            {answer.duty != null
              ? `Estimated duty: $${answer.duty}`
              : `Duty unknown (${answer.status}). ${answer.missing?.join(" ") ?? ""}`}
          </p>
          <ul>
            {answer.lines?.map(({ name, amount }) => (
              <li key={name}>
                {name}: {amount === null ? "unknown" : `$${amount}`}
              </li>
            ))}
          </ul>
        </>
      )}
    </main>
  );
}
