// The client: the key, the retries, the idempotency key and the errors around each operation.

import type { Call } from "./call.js";
import {
  APIConnectionError,
  APIError,
  APITimeoutError,
  AuthenticationError,
  BY_STATUS,
  TariffTrustError,
} from "./errors.js";
import { Operations } from "./operations.js";
import { VERSION } from "./version.js";

const DEFAULT_BASE_URL = "https://api.tarifftrust.com";
// What a gateway answers when the service behind it is away, without the API's error.
const GATEWAY_STATUSES = new Set([429, 502, 503, 504]);

export interface ClientOptions {
  /** The key, or TARIFFTRUST_API_KEY. Keep it on your server. Only getStatus works without one. */
  apiKey?: string;
  /** The API's address, or TARIFFTRUST_BASE_URL; the production's otherwise. */
  baseUrl?: string;
  /** The milliseconds a whole attempt may take. Default: 60000. */
  timeoutMs?: number;
  /**
   * How many times a call is tried again: after a connection failure, a timeout or a gateway error,
   * or when the API gives a Retry-After. An idempotency key makes these retries count once.
   * Default: 2.
   */
  maxRetries?: number;
  /** The longest Retry-After waited for, in seconds; a longer one is raised. Default: 60. */
  maxRetryWaitSeconds?: number;
  /** Your own fetch (a proxy, your certificates). */
  fetch?: typeof globalThis.fetch;
}

function environment(name: string): string | undefined {
  const scope = globalThis as { process?: { env?: Record<string, string | undefined> } };
  return scope.process?.env?.[name];
}

function backoff(attempt: number): number {
  return Math.min(500 * 2 ** attempt, 8000) * (0.5 + Math.random() / 2);
}

function sleep(milliseconds: number, signal?: AbortSignal): Promise<void> {
  return new Promise((resolve, reject) => {
    const done = () => {
      signal?.removeEventListener("abort", stop);
      resolve();
    };
    const timer = setTimeout(done, milliseconds);
    const stop = () => {
      clearTimeout(timer);
      reject(signal?.reason);
    };
    if (signal?.aborted) return stop();
    signal?.addEventListener("abort", stop, { once: true });
  });
}

function refusal(status: number, headers: Headers, text: string): APIError {
  let body: unknown;
  try {
    body = JSON.parse(text);
  } catch {
    body = null;
  }
  const answer = (typeof body === "object" && body !== null ? body : {}) as Record<string, unknown>;
  // The error of a proxy may be a plain string: only an object is the API's.
  const error = (typeof answer["error"] === "object" && answer["error"] !== null
    ? answer["error"]
    : {}) as { code?: string; message?: string; fields?: string[] };
  const retryAfter = headers.get("Retry-After") ?? "";
  const Kind = BY_STATUS[status] ?? APIError;
  return new Kind(error.message || `HTTP ${status}`, {
    status,
    code: error.code,
    fields: error.fields,
    requestId: (answer["request_id"] as string | undefined) ?? headers.get("X-Request-ID"),
    retryAfter: /^\d+$/.test(retryAfter) ? Number(retryAfter) : null,
    body,
  });
}

function runtimeName(): string {
  const scope = globalThis as { process?: { version?: string } };
  return scope.process?.version ? `node/${scope.process.version.replace(/^v/, "")}` : "unknown";
}

/** The TariffTrust API. Each operation of the API is a method under its operationId in camelCase. */
export class TariffTrust extends Operations {
  // Truly private, so that logging a client never prints the key.
  readonly #apiKey: string | undefined;
  private readonly baseUrl: string;
  private readonly timeoutMs: number;
  private readonly maxRetries: number;
  private readonly maxRetryWaitSeconds: number;
  private readonly fetch: typeof globalThis.fetch;

  constructor(options: ClientOptions = {}) {
    super();
    // A stray newline would be refused as a header.
    this.#apiKey = (options.apiKey || environment("TARIFFTRUST_API_KEY"))?.trim() || undefined;
    const baseUrl = options.baseUrl || environment("TARIFFTRUST_BASE_URL") || DEFAULT_BASE_URL;
    this.baseUrl = baseUrl.replace(/\/+$/, "");
    this.timeoutMs = options.timeoutMs ?? 60_000;
    this.maxRetries = options.maxRetries ?? 2;
    this.maxRetryWaitSeconds = options.maxRetryWaitSeconds ?? 60;
    // Called as a plain function: some runtimes refuse a fetch called as a method of another object.
    const found = options.fetch;
    this.fetch = found ? (url, init) => found(url, init) : (url, init) => globalThis.fetch(url, init);
  }

  /** The milliseconds before trying again after a refusal, null when trying again cannot help. */
  private waitBeforeRetry(error: APIError, attempt: number): number | null {
    if (error.retryAfter !== null) {
      return error.retryAfter <= this.maxRetryWaitSeconds ? error.retryAfter * 1000 : null;
    }
    return error.code === null && GATEWAY_STATUSES.has(error.status) ? backoff(attempt) : null;
  }

  private url(call: Call): string {
    const query = new URLSearchParams();
    for (const [name, value] of Object.entries(call.query ?? {})) {
      if (value !== undefined && value !== null) query.set(name, String(value));
    }
    const search = query.toString();
    return `${this.baseUrl}${call.path}${search ? `?${search}` : ""}`;
  }

  private headers(call: Call): Record<string, string> {
    const headers: Record<string, string> = {
      Accept: "application/json",
      "User-Agent": `tarifftrust-node/${VERSION} ${runtimeName()}`,
    };
    if (call.auth !== false) {
      if (!this.#apiKey) {
        throw new AuthenticationError("No API key: pass apiKey or set TARIFFTRUST_API_KEY", {
          status: 401,
        });
      }
      headers["Authorization"] = `Bearer ${this.#apiKey}`;
    }
    // The call's key: every attempt sends the same one, so that a retry counts once.
    if (call.idempotent) {
      const given = call.options?.idempotencyKey;
      // eslint-disable-next-line no-control-regex
      if (given && !/^[\x00-\x7f]*$/.test(given)) {
        throw new RangeError("An idempotency key is a header: use only ASCII characters");
      }
      headers["Idempotency-Key"] = given || globalThis.crypto.randomUUID();
    }
    if (call.body !== undefined) headers["Content-Type"] = "application/json";
    return headers;
  }

  protected async request<T>(call: Call): Promise<T> {
    const url = this.url(call);
    const headers = this.headers(call);
    const body = call.body === undefined ? undefined : JSON.stringify(call.body);
    const caller = call.options?.signal;
    for (let attempt = 0; ; attempt += 1) {
      const timeout = AbortSignal.timeout(call.options?.timeoutMs ?? this.timeoutMs);
      const signal = caller ? AbortSignal.any([caller, timeout]) : timeout;
      let wait: number;
      try {
        const response = await this.fetch(url, {
          method: call.method,
          headers,
          signal,
          // A redirect is an answer to report: following it would turn a POST into a GET.
          redirect: "manual",
          ...(body === undefined ? {} : { body }),
        });
        const text = await response.text();
        if (response.ok) return parse<T>(text, response.status);
        const error = refusal(response.status, response.headers, text);
        const found = this.waitBeforeRetry(error, attempt);
        if (found === null || attempt >= this.maxRetries) throw error;
        wait = found;
      } catch (failure) {
        if (failure instanceof TariffTrustError || caller?.aborted) throw failure;
        if (attempt >= this.maxRetries) {
          const options = { cause: failure };
          if (timeout.aborted) {
            throw new APITimeoutError("The API did not answer in time", options);
          }
          throw new APIConnectionError(`The API could not be reached: ${String(failure)}`, options);
        }
        wait = backoff(attempt);
      }
      await sleep(wait, caller);
    }
  }
}

function parse<T>(text: string, status: number): T {
  try {
    return JSON.parse(text) as T;
  } catch (cause) {
    throw new TariffTrustError(`The API's answer is not JSON (HTTP ${status})`, { cause });
  }
}
