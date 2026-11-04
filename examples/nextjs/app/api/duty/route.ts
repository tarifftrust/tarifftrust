// A route handler: the API key stays on the server, the browser only ever calls this route.
import { NextResponse } from "next/server";
import { InvalidInputError, TariffTrust } from "tarifftrust";

const client = new TariffTrust();

export async function POST(request: Request) {
  const { hts, origin, customs_value } = (await request.json()) as {
    hts?: string;
    origin?: string;
    customs_value?: string;
  };
  if (!hts || !origin) {
    return NextResponse.json({ error: "An HTS code and an origin are required" }, { status: 400 });
  }
  try {
    const result = await client.estimate({ hts, origin, customs_value: customs_value || null });
    return NextResponse.json({
      status: result.status,
      duty: result.estimated_duty,
      lines: (result.duties ?? []).map(({ name, amount }) => ({ name, amount })),
      missing: (result.missing ?? []).map(({ question }) => question),
    });
  } catch (error) {
    if (error instanceof InvalidInputError) {
      return NextResponse.json({ error: error.message, fields: error.fields }, { status: 422 });
    }
    // Refused or out of reach: the request id, if any, is what to quote to TariffTrust's support.
    console.error(String(error));
    return NextResponse.json({ error: "Duties are not available right now" }, { status: 502 });
  }
}
