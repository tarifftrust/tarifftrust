// What an operation asks of the client, and what a caller may add to one call.

export interface RequestOptions {
  /** Makes a retry of this call safe; a new one is generated for each call otherwise. */
  idempotencyKey?: string;
  /** Cancels the call. */
  signal?: AbortSignal;
  /** The milliseconds an attempt may take, instead of the client's. */
  timeoutMs?: number;
}

export interface Call {
  method: string;
  path: string;
  body?: unknown;
  query?: Record<string, unknown>;
  auth?: boolean;
  idempotent?: boolean;
  options?: RequestOptions | undefined;
}
