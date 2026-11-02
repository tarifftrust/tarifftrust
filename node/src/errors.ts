// What a call may raise: the API's refusals by their status, and the failures to reach it.

/**
 * What a call raises when the API refuses it or cannot be reached. An argument that cannot be sent
 * at all is a TypeError or a RangeError, before any request.
 */
export class TariffTrustError extends Error {
  constructor(message: string, options?: ErrorOptions) {
    super(message, options);
    this.name = new.target.name;
  }
}

/** The API could not be reached, after the retries. */
export class APIConnectionError extends TariffTrustError {}

/** The API did not answer in time, after the retries. */
export class APITimeoutError extends APIConnectionError {}

export interface APIErrorDetails {
  status: number;
  code?: string | null | undefined;
  fields?: string[] | null | undefined;
  requestId?: string | null | undefined;
  retryAfter?: number | null | undefined;
  body?: unknown;
}

/**
 * The API refused the request. `code` is for a program, `message` for a person, `fields` names what
 * invalid_input refused, `requestId` is what to quote to support, and `retryAfter` the seconds to
 * wait when trying again helps, null otherwise.
 */
export class APIError extends TariffTrustError {
  readonly status: number;
  readonly code: string | null;
  readonly fields: string[];
  readonly requestId: string | null;
  readonly retryAfter: number | null;
  readonly body: unknown;

  constructor(message: string, details: APIErrorDetails) {
    super(message);
    this.status = details.status;
    this.code = details.code ?? null;
    this.fields = details.fields ?? [];
    this.requestId = details.requestId ?? null;
    this.retryAfter = details.retryAfter ?? null;
    this.body = details.body;
  }

  /** The whole refusal, for a log: its code, its message, its status and its request id. */
  override toString(): string {
    const parts = [`HTTP ${this.status}`];
    if (this.fields.length) parts.push(`fields: ${this.fields.join(", ")}`);
    if (this.requestId) parts.push(`request ${this.requestId}`);
    return `${this.code ? `${this.code}: ` : ""}${this.message} (${parts.join("; ")})`;
  }
}

/** 401: no valid API key. */
export class AuthenticationError extends APIError {}

/** 402: no active subscription, or the quota is used up (code `quota_exceeded`). */
export class AccessRequiredError extends APIError {}

/** 403: the key lacks the permission, or the plan the API. */
export class PermissionDeniedError extends APIError {}

/** 404: nothing of that name. */
export class NotFoundError extends APIError {}

/** 409: an idempotency key sent again with another request. */
export class ConflictError extends APIError {}

/** 413: the body is larger than the API takes: send fewer products or lines. */
export class PayloadTooLargeError extends APIError {}

/** 422: `fields` names each field refused; 400: the body is not valid JSON. */
export class InvalidInputError extends APIError {}

/** 429: too many requests. */
export class RateLimitError extends APIError {}

/** 502, 503 or 504: unavailable for now. */
export class ServiceUnavailableError extends APIError {}

export const BY_STATUS: Record<number, typeof APIError> = {
  400: InvalidInputError,
  401: AuthenticationError,
  402: AccessRequiredError,
  403: PermissionDeniedError,
  404: NotFoundError,
  409: ConflictError,
  413: PayloadTooLargeError,
  422: InvalidInputError,
  429: RateLimitError,
  502: ServiceUnavailableError,
  503: ServiceUnavailableError,
  504: ServiceUnavailableError,
};
