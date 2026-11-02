// Official Node.js and TypeScript client for the TariffTrust API: every US import duty and fee for
// an HTS code, an origin and a value, each with its official source. https://tarifftrust.com/api/

export type { RequestOptions } from "./call.js";
export type { ClientOptions } from "./client.js";
export { TariffTrust } from "./client.js";
export {
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
  TariffTrustError,
} from "./errors.js";
export type * from "./types.js";
export { VERSION } from "./version.js";
