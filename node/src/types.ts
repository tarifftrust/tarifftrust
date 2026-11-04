// The objects of the TariffTrust API. Generated from openapi.json by scripts/generate.py: do not edit.

/**
 * A trade agreement, by its symbol in the HTS special column.
 */
export interface Agreement {
  /**
   * A product agreement open to any column 1 origin.
   */
  any_column1_origin: boolean;
  /**
   * The agreement's common name, where it has one.
   */
  name: string | null;
  /**
   * The origins it can apply to; none for a product agreement.
   */
  origins: string[];
  /**
   * As the HTS special column prints it; send it as preference.
   */
  symbol: string;
}

/**
 * The trade agreements the engine applies.
 */
export interface AgreementList {
  /**
   * Each agreement the engine applies.
   */
  agreements: Agreement[];
  /**
   * What a symbol does not establish.
   */
  condition: string;
  /**
   * Where the tariff that names them is published.
   */
  source: string;
}

/**
 * A saved declaration's answer, with the detail behind it.
 */
export interface AuditedDeclaration {
  /**
   * The day calculated, in New York.
   */
  as_of: string;
  /**
   * The detail behind the answer, kept with a saved estimate: the measures examined with the
   * decision and the reason of each, every duty and fee in full, the answers supposed and what
   * each other answer gives, the sources, the inputs as calculated and the versions.
   */
  audit: Record<string, unknown>;
  data: Data;
  /**
   * formal, unless you send informal. An informal entry has no calculated fees.
   */
  entry_type: string | null;
  /**
   * The duties of every line, in US dollars.
   */
  estimated_duty?: string | null;
  /**
   * Those duties as a fraction of the values.
   */
  estimated_duty_rate?: string | null;
  /**
   * The entry fees of the declaration, in US dollars.
   */
  estimated_fees?: string | null;
  /**
   * Values, duties, fees, freight and insurance, in US dollars.
   */
  estimated_landed_cost?: string | null;
  /**
   * The exemption its fees rest on, when one was declared for it.
   */
  facts?: Record<string, unknown> | null;
  /**
   * Each entry fee, with its amount and source.
   */
  fees?: EntryFee[] | null;
  /**
   * The freight you sent, in US dollars.
   */
  freight?: string | null;
  /**
   * The insurance you sent, in US dollars.
   */
  insurance?: string | null;
  /**
   * While a duty is withheld, the last result established without it.
   */
  last_approved?: LastApproved | null;
  /**
   * Each line, in the order sent, with its detail.
   */
  lines: AuditedLine[];
  /**
   * Your reference for it, when you sent one.
   */
  reference?: string | null;
  /**
   * calculated: every duty is established; without a customs value, a duty that does not need
   * it comes with estimated_fees and estimated_landed_cost null, and a warning says so.
   * rate_only: no customs value was sent, and estimated_duty_rate is the answer; send the value
   * for the amounts. needs_information: something is missing to give a figure, and missing says
   * what to send again, on each line of a declaration. partial: a duty is withheld for now, and
   * withheld says which; no total is given. unsupported: a regime or a rate the service does
   * not calculate. not_found: a code the tariff does not have, or that names no product.
   * not_covered: the date or the chapter is outside the data.
   */
  status: "calculated" | "rate_only" | "needs_information" | "partial" | "unsupported" | "not_found" | "not_covered";
  /**
   * How the goods arrive. Sent, or else supposed: land for Canada and Mexico, ocean otherwise.
   * By sea they pay the HMF.
   */
  transport_mode: string | null;
  /**
   * What the amounts do not cover, in words.
   */
  warnings?: string[] | null;
}

/**
 * A saved estimate's answer, with the detail behind it.
 */
export interface AuditedEstimate {
  /**
   * The day calculated, in New York.
   */
  as_of: string;
  /**
   * The detail behind the answer, kept with a saved estimate: the measures examined with the
   * decision and the reason of each, every duty and fee in full, the answers supposed and what
   * each other answer gives, the sources, the inputs as calculated and the versions.
   */
  audit: Record<string, unknown>;
  /**
   * The longer codes under a short one: send one of them as hts.
   */
  candidates?: Candidate[] | null;
  /**
   * The customs value you sent, in US dollars; null without one.
   */
  customs_value: string | null;
  data: Data;
  /**
   * What the code covers, in the words of the tariff.
   */
  description: string | null;
  /**
   * Each duty, with its rate, amount and source.
   */
  duties?: Duty[] | null;
  /**
   * formal, unless you send informal. An informal entry has no calculated fees.
   */
  entry_type: string | null;
  /**
   * All the duties, in US dollars. Null is unknown, never zero.
   */
  estimated_duty?: string | null;
  /**
   * The duties as a fraction of the customs value: 0.365 is 36.5%. Without a value, the sum of
   * the rates; null when a duty is not a percentage, or while a duty is withheld.
   */
  estimated_duty_rate?: string | null;
  /**
   * All the entry fees, in US dollars; null when one cannot be calculated, or with include_fees
   * false.
   */
  estimated_fees?: string | null;
  /**
   * Customs value, duties, fees, freight and insurance, in US dollars; null when the value or a
   * fee asked for is not known.
   */
  estimated_landed_cost?: string | null;
  /**
   * The answers this estimate rests on, those you sent and those supposed: the ordinary case of
   * each question a rule asks of these goods. Send any of them in facts to change the estimate;
   * GET /v2/facts gives each one's question and answers.
   */
  facts?: Record<string, unknown> | null;
  /**
   * Each entry fee, with its amount and source.
   */
  fees?: EntryFee[] | null;
  /**
   * The freight you sent, in US dollars.
   */
  freight?: string | null;
  /**
   * The HTS code, in digits.
   */
  hts: string;
  /**
   * The insurance you sent, in US dollars.
   */
  insurance?: string | null;
  /**
   * While a duty is withheld, the last result established without it.
   */
  last_approved?: LastApproved | null;
  /**
   * What to send again for a figure, with status needs_information.
   */
  missing?: MissingField[] | null;
  /**
   * The country of origin.
   */
  origin: string;
  /**
   * The quantities you sent.
   */
  quantities?: Record<string, unknown> | null;
  /**
   * calculated: every duty is established; without a customs value, a duty that does not need
   * it comes with estimated_fees and estimated_landed_cost null, and a warning says so.
   * rate_only: no customs value was sent, and estimated_duty_rate is the answer; send the value
   * for the amounts. needs_information: something is missing to give a figure, and missing says
   * what to send again, on each line of a declaration. partial: a duty is withheld for now, and
   * withheld says which; no total is given. unsupported: a regime or a rate the service does
   * not calculate. not_found: a code the tariff does not have, or that names no product.
   * not_covered: the date or the chapter is outside the data.
   */
  status: "calculated" | "rate_only" | "needs_information" | "partial" | "unsupported" | "not_found" | "not_covered";
  /**
   * How the goods arrive. Sent, or else supposed: land for Canada and Mexico, ocean otherwise.
   * By sea they pay the HMF.
   */
  transport_mode: string | null;
  /**
   * What the amounts do not cover, in words.
   */
  warnings?: string[] | null;
  /**
   * What the total leaves out for now.
   */
  withheld?: Withheld[] | null;
}

/**
 * One line of a saved declaration, with the detail behind it.
 */
export interface AuditedLine {
  /**
   * The detail behind the answer, kept with a saved estimate: the measures examined with the
   * decision and the reason of each, every duty and fee in full, the answers supposed and what
   * each other answer gives, the sources, the inputs as calculated and the versions.
   */
  audit: Record<string, unknown>;
  /**
   * The longer codes under a short one: send one of them as hts.
   */
  candidates?: Candidate[] | null;
  /**
   * The customs value you sent, in US dollars; null without one.
   */
  customs_value: string | null;
  /**
   * What the code covers, in the words of the tariff.
   */
  description: string | null;
  /**
   * Each duty, with its rate, amount and source.
   */
  duties?: Duty[] | null;
  /**
   * All the duties, in US dollars. Null is unknown, never zero.
   */
  estimated_duty?: string | null;
  /**
   * The duties as a fraction of the customs value: 0.365 is 36.5%. Without a value, the sum of
   * the rates; null when a duty is not a percentage, or while a duty is withheld.
   */
  estimated_duty_rate?: string | null;
  /**
   * The answers this estimate rests on, those you sent and those supposed: the ordinary case of
   * each question a rule asks of these goods. Send any of them in facts to change the estimate;
   * GET /v2/facts gives each one's question and answers.
   */
  facts?: Record<string, unknown> | null;
  /**
   * The HTS code, in digits.
   */
  hts: string;
  /**
   * What to send again for a figure, with status needs_information.
   */
  missing?: MissingField[] | null;
  /**
   * The country of origin.
   */
  origin: string;
  /**
   * The quantities you sent.
   */
  quantities?: Record<string, unknown> | null;
  /**
   * Your reference for it, when you sent one.
   */
  reference?: string | null;
  /**
   * calculated: every duty is established; without a customs value, a duty that does not need
   * it comes with estimated_fees and estimated_landed_cost null, and a warning says so.
   * rate_only: no customs value was sent, and estimated_duty_rate is the answer; send the value
   * for the amounts. needs_information: something is missing to give a figure, and missing says
   * what to send again, on each line of a declaration. partial: a duty is withheld for now, and
   * withheld says which; no total is given. unsupported: a regime or a rate the service does
   * not calculate. not_found: a code the tariff does not have, or that names no product.
   * not_covered: the date or the chapter is outside the data.
   */
  status: "calculated" | "rate_only" | "needs_information" | "partial" | "unsupported" | "not_found" | "not_covered";
  /**
   * What the amounts do not cover, in words.
   */
  warnings?: string[] | null;
  /**
   * What the total leaves out for now.
   */
  withheld?: Withheld[] | null;
}

/**
 * An item of a batch that could not be calculated.
 */
export interface BatchFailure {
  /**
   * Why.
   */
  error: Error;
  /**
   * Its position in the batch, from 0.
   */
  index: number;
}

/**
 * One product of a batch: the batch's publication, if any, applies to every item.
 */
export interface BatchItem {
  /**
   * When the goods are entered for consumption. A day, in New York time ("2026-04-05"); or, on
   * a day when a measure takes effect at a stated hour, the instant of entry with its UTC
   * offset ("2026-04-05T00:01:00-04:00"). Unset: today.
   */
  as_of?: string | null;
  /**
   * Customs value in US dollars: the transaction value declared, not a retail price. Unset: the
   * duty rate is given, and an amount only where the duty does not depend on the value.
   */
  customs_value?: number | string | null;
  /**
   * A formal entry pays the merchandise processing fee (MPF) on its value. An informal entry
   * pays a fixed fee the estimate does not calculate: it gives no fees.
   *
   * Default: "formal".
   */
  entry_type?: "formal" | "informal";
  /**
   * Answers to the questions of the facts catalogue (GET /v2/facts), by name. A name outside
   * the catalogue is said in warnings and never used.
   */
  facts?: Record<string, number | string | boolean>;
  /**
   * International freight in US dollars: no duty on it, it adds to the landed cost.
   *
   * Default: "0".
   */
  freight?: number | string;
  /**
   * The HTS code of the goods: 4, 6, 8 or 10 digits, dots and spaces ignored. A rate needs the
   * 10-digit statistical line or its 8-digit subheading.
   */
  hts: string;
  /**
   * Count the entry fees (MPF, HMF) of a declaration of this product alone. Each product is
   * estimated as its own declaration: the MPF is charged once on a declaration, so for several
   * products entered together use POST /v2/estimates/entry.
   *
   * Default: true.
   */
  include_fees?: boolean;
  /**
   * Insurance of the shipment in US dollars: no duty on it, it adds to the landed cost.
   *
   * Default: "0".
   */
  insurance?: number | string;
  /**
   * A name for the saved estimate; needs save.
   */
  label?: string;
  /**
   * Country of origin: where the goods were produced, not where they ship from. ISO 3166-1
   * alpha-2 (XK for Kosovo), or a code U.S. Customs files with (BU, GZ, KV, WE).
   */
  origin: string;
  /**
   * A trade agreement's symbol from the HTS special column (S for USMCA, KR for KORUS…; GET
   * /v2/agreements). Giving it declares that the goods meet its rules of origin and that you
   * hold the proof.
   */
  preference?: string | null;
  /**
   * Quantities in the units a duty counts (kg, l, item, dozen, pair, proof_liter…),
   * nonnegative. An answer names the quantity it needs in missing ("quantities.kg").
   */
  quantities?: Record<string, number | string>;
  /**
   * Save the estimate: only a saved estimate keeps its detail, is reported, and is notified if
   * a rate proves wrong. An answer without a figure is not saved. Send an Idempotency-Key:
   * without one, a request sent again after a timeout saves twice.
   *
   * Default: false.
   */
  save?: boolean;
  /**
   * How the goods arrive; by sea they also pay the harbor maintenance fee (HMF). Unset: land
   * for goods of Canada or Mexico, ocean otherwise.
   */
  transport_mode?: "air" | "ocean" | "land" | null;
}

/**
 * Up to 200 products, each calculated on its own: POST /v2/estimates/batch.
 */
export interface BatchRequest {
  /**
   * The products, each calculated on its own.
   */
  items: BatchItem[];
  /**
   * Calculate with this publication of the rules instead of the one in service on that date:
   * the data.publication_id of an earlier answer gives the same result again, as long as the
   * engine has not changed.
   */
  publication_id?: string | null;
}

/**
 * Each item of a batch, in the order sent.
 */
export interface BatchResult {
  /**
   * Each item, its estimate or its error.
   */
  results: (BatchSuccess | BatchFailure)[];
}

/**
 * An item of a batch that was calculated.
 */
export interface BatchSuccess {
  /**
   * Its position in the batch, from 0.
   */
  index: number;
  /**
   * Its estimate, as POST /v2/estimates gives it, without last_approved.
   */
  result: Estimate;
}

/**
 * A longer code under a short one.
 */
export interface Candidate {
  /**
   * What it covers, in the words of the tariff.
   */
  description: string | null;
  /**
   * The code, in digits.
   */
  hts: string;
}

/**
 * A period the service holds rules for, and the publication that covers it.
 */
export interface CoveredWindow {
  /**
   * Its first day.
   */
  from: string;
  /**
   * The publication used over this window.
   */
  publication_id: string;
  /**
   * Its last day.
   */
  through: string;
}

/**
 * The data the answer rests on.
 */
export interface Data {
  /**
   * When the official sources were last checked; null for a past edition.
   */
  checked_at?: string | null;
  /**
   * The edition of the US tariff, in words.
   */
  edition: string | null;
  /**
   * The publication of the rules it was calculated with: send it as publication_id to calculate
   * again with the same rules.
   */
  publication_id: string | null;
  /**
   * True when those checks are older than they should be.
   */
  stale?: boolean | null;
}

/**
 * The estimate of a whole import declaration: each line, and its fees once.
 */
export interface Declaration {
  /**
   * The day calculated, in New York.
   */
  as_of: string;
  data: Data;
  /**
   * formal, unless you send informal. An informal entry has no calculated fees.
   */
  entry_type: string | null;
  /**
   * The duties of every line, in US dollars.
   */
  estimated_duty?: string | null;
  /**
   * Those duties as a fraction of the values.
   */
  estimated_duty_rate?: string | null;
  /**
   * The entry fees of the declaration, in US dollars.
   */
  estimated_fees?: string | null;
  /**
   * Values, duties, fees, freight and insurance, in US dollars.
   */
  estimated_landed_cost?: string | null;
  /**
   * The exemption its fees rest on, when one was declared for it.
   */
  facts?: Record<string, unknown> | null;
  /**
   * Each entry fee, with its amount and source.
   */
  fees?: EntryFee[] | null;
  /**
   * The freight you sent, in US dollars.
   */
  freight?: string | null;
  /**
   * The insurance you sent, in US dollars.
   */
  insurance?: string | null;
  /**
   * While a duty is withheld, the last result established without it.
   */
  last_approved?: LastApproved | null;
  /**
   * Each line, in the order sent.
   */
  lines: Line[];
  /**
   * Your reference for it, when you sent one.
   */
  reference?: string | null;
  /**
   * Sent with save: its identifier, to read it with its detail.
   */
  saved_estimate_id?: string | null;
  /**
   * calculated: every duty is established; without a customs value, a duty that does not need
   * it comes with estimated_fees and estimated_landed_cost null, and a warning says so.
   * rate_only: no customs value was sent, and estimated_duty_rate is the answer; send the value
   * for the amounts. needs_information: something is missing to give a figure, and missing says
   * what to send again, on each line of a declaration. partial: a duty is withheld for now, and
   * withheld says which; no total is given. unsupported: a regime or a rate the service does
   * not calculate. not_found: a code the tariff does not have, or that names no product.
   * not_covered: the date or the chapter is outside the data.
   */
  status: "calculated" | "rate_only" | "needs_information" | "partial" | "unsupported" | "not_found" | "not_covered";
  /**
   * How the goods arrive. Sent, or else supposed: land for Canada and Mexico, ocean otherwise.
   * By sea they pay the HMF.
   */
  transport_mode: string | null;
  /**
   * What the amounts do not cover, in words.
   */
  warnings?: string[] | null;
}

/**
 * One duty of the estimate.
 */
export interface Duty {
  /**
   * Its amount in US dollars; null when it cannot be calculated yet.
   */
  amount: string | null;
  /**
   * Its Chapter 99 heading; null for the base duty.
   */
  heading: string | null;
  /**
   * What the duty is, in words.
   */
  name: string;
  /**
   * Its rate, as a person reads it.
   */
  rate: string | null;
  /**
   * The official document it rests on.
   */
  source: Source | null;
}

/**
 * One entry fee of the declaration.
 */
export interface EntryFee {
  /**
   * Its amount in US dollars; null when it cannot be calculated yet.
   */
  amount: string | null;
  /**
   * What the fee is, in words: the merchandise processing fee (MPF) or the harbor maintenance
   * fee (HMF).
   */
  name: string;
  /**
   * Why its amount is what it is, when that needs saying.
   */
  note?: string | null;
  /**
   * The official document it rests on.
   */
  source: Source | null;
}

/**
 * A whole import declaration: POST /v2/estimates/entry.
 */
export interface EntryRequest {
  /**
   * When the goods are entered for consumption. A day, in New York time ("2026-04-05"); or, on
   * a day when a measure takes effect at a stated hour, the instant of entry with its UTC
   * offset ("2026-04-05T00:01:00-04:00"). Unset: today.
   */
  as_of?: string | null;
  /**
   * A formal entry pays the merchandise processing fee (MPF) on its value. An informal entry
   * pays a fixed fee the estimate does not calculate: it gives no fees.
   *
   * Default: "formal".
   */
  entry_type?: "formal" | "informal";
  /**
   * Answers that hold for the whole declaration (GET /v2/facts, scope entry or shipment).
   */
  facts?: Record<string, number | string | boolean>;
  /**
   * International freight in US dollars: no duty on it, it adds to the landed cost.
   *
   * Default: "0".
   */
  freight?: number | string;
  /**
   * Count the entry fees (MPF, HMF) of the declaration.
   *
   * Default: true.
   */
  include_fees?: boolean;
  /**
   * Insurance of the shipment in US dollars: no duty on it, it adds to the landed cost.
   *
   * Default: "0".
   */
  insurance?: number | string;
  /**
   * A name for the saved estimate; needs save.
   */
  label?: string;
  /**
   * The lines of the declaration, each a product.
   */
  lines: LineInput[];
  /**
   * Calculate with this publication of the rules instead of the one in service on that date:
   * the data.publication_id of an earlier answer gives the same result again, as long as the
   * engine has not changed.
   */
  publication_id?: string | null;
  /**
   * Your reference for the declaration.
   */
  reference?: string;
  /**
   * Save the estimate: only a saved estimate keeps its detail, is reported, and is notified if
   * a rate proves wrong. An answer without a figure is not saved. Send an Idempotency-Key:
   * without one, a request sent again after a timeout saves twice.
   *
   * Default: false.
   */
  save?: boolean;
  /**
   * How the goods arrive; by sea they also pay the harbor maintenance fee (HMF). Unset: land
   * for goods of Canada or Mexico, ocean otherwise.
   */
  transport_mode?: "air" | "ocean" | "land" | null;
}

/**
 * What was refused, and why.
 */
export interface Error {
  /**
   * What went wrong, for a program: invalid_input, quota_exceeded, rate_limited,
   * data_unavailable…
   */
  code: string;
  /**
   * With invalid_input: each field refused, by its path (items.3.hts).
   */
  fields?: string[] | null;
  /**
   * The same in words, for a person.
   */
  message?: string | null;
}

/**
 * Every error of the API.
 */
export interface ErrorResponse {
  /**
   * The error.
   */
  error: Error;
  /**
   * The request's identifier, also in X-Request-ID: quote it to support.
   */
  request_id?: string | null;
}

/**
 * The estimate of one product.
 */
export interface Estimate {
  /**
   * The day calculated, in New York.
   */
  as_of: string;
  /**
   * The longer codes under a short one: send one of them as hts.
   */
  candidates?: Candidate[] | null;
  /**
   * The customs value you sent, in US dollars; null without one.
   */
  customs_value: string | null;
  data: Data;
  /**
   * What the code covers, in the words of the tariff.
   */
  description: string | null;
  /**
   * Each duty, with its rate, amount and source.
   */
  duties?: Duty[] | null;
  /**
   * formal, unless you send informal. An informal entry has no calculated fees.
   */
  entry_type: string | null;
  /**
   * All the duties, in US dollars. Null is unknown, never zero.
   */
  estimated_duty?: string | null;
  /**
   * The duties as a fraction of the customs value: 0.365 is 36.5%. Without a value, the sum of
   * the rates; null when a duty is not a percentage, or while a duty is withheld.
   */
  estimated_duty_rate?: string | null;
  /**
   * All the entry fees, in US dollars; null when one cannot be calculated, or with include_fees
   * false.
   */
  estimated_fees?: string | null;
  /**
   * Customs value, duties, fees, freight and insurance, in US dollars; null when the value or a
   * fee asked for is not known.
   */
  estimated_landed_cost?: string | null;
  /**
   * The answers this estimate rests on, those you sent and those supposed: the ordinary case of
   * each question a rule asks of these goods. Send any of them in facts to change the estimate;
   * GET /v2/facts gives each one's question and answers.
   */
  facts?: Record<string, unknown> | null;
  /**
   * Each entry fee, with its amount and source.
   */
  fees?: EntryFee[] | null;
  /**
   * The freight you sent, in US dollars.
   */
  freight?: string | null;
  /**
   * The HTS code, in digits.
   */
  hts: string;
  /**
   * The insurance you sent, in US dollars.
   */
  insurance?: string | null;
  /**
   * While a duty is withheld, the last result established without it.
   */
  last_approved?: LastApproved | null;
  /**
   * What to send again for a figure, with status needs_information.
   */
  missing?: MissingField[] | null;
  /**
   * The country of origin.
   */
  origin: string;
  /**
   * The quantities you sent.
   */
  quantities?: Record<string, unknown> | null;
  /**
   * Sent with save: its identifier, to read it with its detail.
   */
  saved_estimate_id?: string | null;
  /**
   * calculated: every duty is established; without a customs value, a duty that does not need
   * it comes with estimated_fees and estimated_landed_cost null, and a warning says so.
   * rate_only: no customs value was sent, and estimated_duty_rate is the answer; send the value
   * for the amounts. needs_information: something is missing to give a figure, and missing says
   * what to send again, on each line of a declaration. partial: a duty is withheld for now, and
   * withheld says which; no total is given. unsupported: a regime or a rate the service does
   * not calculate. not_found: a code the tariff does not have, or that names no product.
   * not_covered: the date or the chapter is outside the data.
   */
  status: "calculated" | "rate_only" | "needs_information" | "partial" | "unsupported" | "not_found" | "not_covered";
  /**
   * How the goods arrive. Sent, or else supposed: land for Canada and Mexico, ocean otherwise.
   * By sea they pay the HMF.
   */
  transport_mode: string | null;
  /**
   * What the amounts do not cover, in words.
   */
  warnings?: string[] | null;
  /**
   * What the total leaves out for now.
   */
  withheld?: Withheld[] | null;
}

/**
 * One product at a date: POST /v2/estimates.
 */
export interface EstimateRequest {
  /**
   * When the goods are entered for consumption. A day, in New York time ("2026-04-05"); or, on
   * a day when a measure takes effect at a stated hour, the instant of entry with its UTC
   * offset ("2026-04-05T00:01:00-04:00"). Unset: today.
   */
  as_of?: string | null;
  /**
   * Customs value in US dollars: the transaction value declared, not a retail price. Unset: the
   * duty rate is given, and an amount only where the duty does not depend on the value.
   */
  customs_value?: number | string | null;
  /**
   * A formal entry pays the merchandise processing fee (MPF) on its value. An informal entry
   * pays a fixed fee the estimate does not calculate: it gives no fees.
   *
   * Default: "formal".
   */
  entry_type?: "formal" | "informal";
  /**
   * Answers to the questions of the facts catalogue (GET /v2/facts), by name. A name outside
   * the catalogue is said in warnings and never used.
   */
  facts?: Record<string, number | string | boolean>;
  /**
   * International freight in US dollars: no duty on it, it adds to the landed cost.
   *
   * Default: "0".
   */
  freight?: number | string;
  /**
   * The HTS code of the goods: 4, 6, 8 or 10 digits, dots and spaces ignored. A rate needs the
   * 10-digit statistical line or its 8-digit subheading.
   */
  hts: string;
  /**
   * Count the entry fees (MPF, HMF) of a declaration of this product alone. Each product is
   * estimated as its own declaration: the MPF is charged once on a declaration, so for several
   * products entered together use POST /v2/estimates/entry.
   *
   * Default: true.
   */
  include_fees?: boolean;
  /**
   * Insurance of the shipment in US dollars: no duty on it, it adds to the landed cost.
   *
   * Default: "0".
   */
  insurance?: number | string;
  /**
   * A name for the saved estimate; needs save.
   */
  label?: string;
  /**
   * Country of origin: where the goods were produced, not where they ship from. ISO 3166-1
   * alpha-2 (XK for Kosovo), or a code U.S. Customs files with (BU, GZ, KV, WE).
   */
  origin: string;
  /**
   * A trade agreement's symbol from the HTS special column (S for USMCA, KR for KORUS…; GET
   * /v2/agreements). Giving it declares that the goods meet its rules of origin and that you
   * hold the proof.
   */
  preference?: string | null;
  /**
   * Calculate with this publication of the rules instead of the one in service on that date:
   * the data.publication_id of an earlier answer gives the same result again, as long as the
   * engine has not changed.
   */
  publication_id?: string | null;
  /**
   * Quantities in the units a duty counts (kg, l, item, dozen, pair, proof_liter…),
   * nonnegative. An answer names the quantity it needs in missing ("quantities.kg").
   */
  quantities?: Record<string, number | string>;
  /**
   * Save the estimate: only a saved estimate keeps its detail, is reported, and is notified if
   * a rate proves wrong. An answer without a figure is not saved. Send an Idempotency-Key:
   * without one, a request sent again after a timeout saves twice.
   *
   * Default: false.
   */
  save?: boolean;
  /**
   * How the goods arrive; by sea they also pay the harbor maintenance fee (HMF). Unset: land
   * for goods of Canada or Mexico, ocean otherwise.
   */
  transport_mode?: "air" | "ocean" | "land" | null;
}

/**
 * One answer a choice question takes.
 */
export interface FactChoice {
  /**
   * The choice in words.
   */
  label?: string | null;
  /**
   * The value to send in facts.
   */
  value: unknown;
}

/**
 * A question an estimate may ask about the goods or the declaration.
 */
export interface FactDefinition {
  /**
   * For a choice: the values to choose from.
   */
  choices?: FactChoice[];
  /**
   * The ordinary case, supposed when unanswered.
   */
  default?: unknown;
  /**
   * What it means, and how to answer it.
   */
  help: string;
  /**
   * The key to answer it with, in facts.
   */
  name: string;
  /**
   * The question to ask.
   */
  question: string;
  /**
   * product: a line's own; entry or shipment: the whole declaration's, one value for all its
   * lines.
   */
  scope: string;
  /**
   * How it is answered: boolean (true or false), choice (one of choices), money (US dollars),
   * number, country (ISO code) or heading (a Chapter 99 heading).
   */
  type: string;
  /**
   * The unit of a number, if any.
   */
  unit?: string;
}

/**
 * The facts catalogue: every question an estimate may ask.
 */
export interface FactList {
  /**
   * Every question of the catalogue.
   */
  facts: FactDefinition[];
}

/**
 * The product at one change of the tariff.
 */
export interface HistoryPoint {
  /**
   * The day calculated, in New York.
   */
  as_of: string;
  /**
   * The longer codes under a short one: send one of them as hts.
   */
  candidates?: Candidate[] | null;
  /**
   * The customs value you sent, in US dollars; null without one.
   */
  customs_value: string | null;
  data: Data;
  /**
   * What the code covers, in the words of the tariff.
   */
  description: string | null;
  /**
   * Each duty, with its rate, amount and source.
   */
  duties?: Duty[] | null;
  /**
   * formal, unless you send informal. An informal entry has no calculated fees.
   */
  entry_type: string | null;
  /**
   * All the duties, in US dollars. Null is unknown, never zero.
   */
  estimated_duty?: string | null;
  /**
   * The duties as a fraction of the customs value: 0.365 is 36.5%. Without a value, the sum of
   * the rates; null when a duty is not a percentage, or while a duty is withheld.
   */
  estimated_duty_rate?: string | null;
  /**
   * All the entry fees, in US dollars; null when one cannot be calculated, or with include_fees
   * false.
   */
  estimated_fees?: string | null;
  /**
   * Customs value, duties, fees, freight and insurance, in US dollars; null when the value or a
   * fee asked for is not known.
   */
  estimated_landed_cost?: string | null;
  /**
   * The answers this estimate rests on, those you sent and those supposed: the ordinary case of
   * each question a rule asks of these goods. Send any of them in facts to change the estimate;
   * GET /v2/facts gives each one's question and answers.
   */
  facts?: Record<string, unknown> | null;
  /**
   * Each entry fee, with its amount and source.
   */
  fees?: EntryFee[] | null;
  /**
   * The freight you sent, in US dollars.
   */
  freight?: string | null;
  /**
   * The HTS code, in digits.
   */
  hts: string;
  /**
   * The insurance you sent, in US dollars.
   */
  insurance?: string | null;
  /**
   * What the IEEPA duties amount to that day, in US dollars; null when not established.
   */
  known_ieepa_duty?: string | null;
  /**
   * While a duty is withheld, the last result established without it.
   */
  last_approved?: LastApproved | null;
  /**
   * What to send again for a figure, with status needs_information.
   */
  missing?: MissingField[] | null;
  /**
   * The country of origin.
   */
  origin: string;
  /**
   * The quantities you sent.
   */
  quantities?: Record<string, unknown> | null;
  /**
   * calculated: every duty is established; without a customs value, a duty that does not need
   * it comes with estimated_fees and estimated_landed_cost null, and a warning says so.
   * rate_only: no customs value was sent, and estimated_duty_rate is the answer; send the value
   * for the amounts. needs_information: something is missing to give a figure, and missing says
   * what to send again, on each line of a declaration. partial: a duty is withheld for now, and
   * withheld says which; no total is given. unsupported: a regime or a rate the service does
   * not calculate. not_found: a code the tariff does not have, or that names no product.
   * not_covered: the date or the chapter is outside the data.
   */
  status: "calculated" | "rate_only" | "needs_information" | "partial" | "unsupported" | "not_found" | "not_covered";
  /**
   * How the goods arrive. Sent, or else supposed: land for Canada and Mexico, ocean otherwise.
   * By sea they pay the HMF.
   */
  transport_mode: string | null;
  /**
   * What the amounts do not cover, in words.
   */
  warnings?: string[] | null;
  /**
   * What the total leaves out for now.
   */
  withheld?: Withheld[] | null;
}

/**
 * One product at every change of the US tariff over a period: POST /v2/estimates/history.
 */
export interface HistoryRequest {
  /**
   * Customs value in US dollars: the transaction value declared, not a retail price. Unset: the
   * duty rate is given, and an amount only where the duty does not depend on the value.
   */
  customs_value?: number | string | null;
  /**
   * A formal entry pays the merchandise processing fee (MPF) on its value. An informal entry
   * pays a fixed fee the estimate does not calculate: it gives no fees.
   *
   * Default: "formal".
   */
  entry_type?: "formal" | "informal";
  /**
   * Answers to the questions of the facts catalogue (GET /v2/facts), by name. A name outside
   * the catalogue is said in warnings and never used.
   */
  facts?: Record<string, number | string | boolean>;
  /**
   * International freight in US dollars: no duty on it, it adds to the landed cost.
   *
   * Default: "0".
   */
  freight?: number | string;
  /**
   * First day of the period. Unset: the first edition the service holds.
   */
  from?: string | null;
  /**
   * The HTS code of the goods: 4, 6, 8 or 10 digits, dots and spaces ignored. A rate needs the
   * 10-digit statistical line or its 8-digit subheading.
   */
  hts: string;
  /**
   * Count the entry fees (MPF, HMF) of a declaration of this product alone. Each product is
   * estimated as its own declaration: the MPF is charged once on a declaration, so for several
   * products entered together use POST /v2/estimates/entry.
   *
   * Default: true.
   */
  include_fees?: boolean;
  /**
   * Insurance of the shipment in US dollars: no duty on it, it adds to the landed cost.
   *
   * Default: "0".
   */
  insurance?: number | string;
  /**
   * Country of origin: where the goods were produced, not where they ship from. ISO 3166-1
   * alpha-2 (XK for Kosovo), or a code U.S. Customs files with (BU, GZ, KV, WE).
   */
  origin: string;
  /**
   * A trade agreement's symbol from the HTS special column (S for USMCA, KR for KORUS…; GET
   * /v2/agreements). Giving it declares that the goods meet its rules of origin and that you
   * hold the proof.
   */
  preference?: string | null;
  /**
   * Quantities in the units a duty counts (kg, l, item, dozen, pair, proof_liter…),
   * nonnegative. An answer names the quantity it needs in missing ("quantities.kg").
   */
  quantities?: Record<string, number | string>;
  /**
   * Last day of the period, at most today. Unset: today.
   */
  through?: string | null;
  /**
   * How the goods arrive; by sea they also pay the harbor maintenance fee (HMF). Unset: land
   * for goods of Canada or Mexico, ocean otherwise.
   */
  transport_mode?: "air" | "ocean" | "land" | null;
}

/**
 * The product at every change of the tariff over the period.
 */
export interface HistoryResult {
  /**
   * The periods the data covers, by publication.
   */
  covered_windows: CoveredWindow[];
  /**
   * The product at each change, in order of date.
   */
  points: HistoryPoint[];
}

/**
 * One line of the tariff, with the descriptions above it and its footnotes.
 */
export interface HtsDetail {
  /**
   * 10 digits for a statistical line, 8 for a subheading, 4 or 6 above.
   */
  code: string;
  /**
   * The descriptions from the heading down to the line's own, joined by ›.
   */
  context: string;
  /**
   * The line's own description.
   */
  description: string;
  /**
   * The code as the tariff prints it (6109.10.00.12).
   */
  display_code: string;
  /**
   * The edition of the US tariff, in words.
   */
  edition: string;
  /**
   * The tariff's footnotes for the line.
   */
  footnotes?: unknown[];
  /**
   * Column 1 general rate, as printed.
   */
  general: string;
  /**
   * The descriptions above the line, from the heading down.
   */
  hierarchy: string[];
  /**
   * Column 2 rate.
   */
  other: string;
  /**
   * The code of the line above it.
   */
  parent: string;
  /**
   * The publication in service.
   */
  publication_id: string;
  /**
   * The 8-digit line whose rates a statistical line without its own takes, as the engine reads
   * them; null when the rates are the line's own.
   */
  rate_from: string | null;
  /**
   * Column 1 special rates and the agreements that give them.
   */
  special: string;
  /**
   * The statistical units the tariff prints (No., kg).
   */
  units: string[];
}

/**
 * A line of the US tariff schedule, as its edition prints it.
 */
export interface HtsLine {
  /**
   * 10 digits for a statistical line, 8 for a subheading, 4 or 6 above.
   */
  code: string;
  /**
   * The descriptions from the heading down to the line's own, joined by ›.
   */
  context: string;
  /**
   * The line's own description.
   */
  description: string;
  /**
   * The code as the tariff prints it (6109.10.00.12).
   */
  display_code: string;
  /**
   * Column 1 general rate, as printed.
   */
  general: string;
  /**
   * Column 2 rate.
   */
  other: string;
  /**
   * The code of the line above it.
   */
  parent: string;
  /**
   * Column 1 special rates and the agreements that give them.
   */
  special: string;
  /**
   * The statistical units the tariff prints (No., kg).
   */
  units: string[];
}

/**
 * A page of the lines a search of the tariff finds.
 */
export interface HtsSearch {
  /**
   * How many lines match.
   */
  count: number;
  /**
   * The edition of the US tariff, in words.
   */
  edition: string;
  /**
   * How many lines a page holds, as asked.
   */
  limit: number;
  /**
   * How many lines were skipped, as asked.
   */
  offset: number;
  /**
   * The publication in service.
   */
  publication_id: string;
  /**
   * The lines of this page, in code order.
   */
  results: HtsLine[];
}

/**
 * The last result established without what is withheld now: dated, kept apart, in no total.
 */
export interface LastApproved {
  /**
   * When that publication went into service.
   */
  approved_from: string | null;
  /**
   * When it left service; null while it serves.
   */
  approved_to: string | null;
  /**
   * The day it was calculated for.
   */
  as_of: string | null;
  /**
   * The edition of the US tariff, in words.
   */
  edition: string | null;
  /**
   * Its duty then, in US dollars.
   */
  estimated_duty: string | null;
  /**
   * Its landed cost then, in US dollars.
   */
  estimated_landed_cost: string | null;
  /**
   * The publication of the rules it was calculated with: send it as publication_id to calculate
   * again with the same rules.
   */
  publication_id: string | null;
  /**
   * Its status then.
   */
  status: "calculated" | "rate_only" | "needs_information" | "partial" | "unsupported" | "not_found" | "not_covered";
}

/**
 * One line of a declaration: its fees are the declaration's.
 */
export interface Line {
  /**
   * The longer codes under a short one: send one of them as hts.
   */
  candidates?: Candidate[] | null;
  /**
   * The customs value you sent, in US dollars; null without one.
   */
  customs_value: string | null;
  /**
   * What the code covers, in the words of the tariff.
   */
  description: string | null;
  /**
   * Each duty, with its rate, amount and source.
   */
  duties?: Duty[] | null;
  /**
   * All the duties, in US dollars. Null is unknown, never zero.
   */
  estimated_duty?: string | null;
  /**
   * The duties as a fraction of the customs value: 0.365 is 36.5%. Without a value, the sum of
   * the rates; null when a duty is not a percentage, or while a duty is withheld.
   */
  estimated_duty_rate?: string | null;
  /**
   * The answers this estimate rests on, those you sent and those supposed: the ordinary case of
   * each question a rule asks of these goods. Send any of them in facts to change the estimate;
   * GET /v2/facts gives each one's question and answers.
   */
  facts?: Record<string, unknown> | null;
  /**
   * The HTS code, in digits.
   */
  hts: string;
  /**
   * What to send again for a figure, with status needs_information.
   */
  missing?: MissingField[] | null;
  /**
   * The country of origin.
   */
  origin: string;
  /**
   * The quantities you sent.
   */
  quantities?: Record<string, unknown> | null;
  /**
   * Your reference for it, when you sent one.
   */
  reference?: string | null;
  /**
   * calculated: every duty is established; without a customs value, a duty that does not need
   * it comes with estimated_fees and estimated_landed_cost null, and a warning says so.
   * rate_only: no customs value was sent, and estimated_duty_rate is the answer; send the value
   * for the amounts. needs_information: something is missing to give a figure, and missing says
   * what to send again, on each line of a declaration. partial: a duty is withheld for now, and
   * withheld says which; no total is given. unsupported: a regime or a rate the service does
   * not calculate. not_found: a code the tariff does not have, or that names no product.
   * not_covered: the date or the chapter is outside the data.
   */
  status: "calculated" | "rate_only" | "needs_information" | "partial" | "unsupported" | "not_found" | "not_covered";
  /**
   * What the amounts do not cover, in words.
   */
  warnings?: string[] | null;
  /**
   * What the total leaves out for now.
   */
  withheld?: Withheld[] | null;
}

/**
 * One line of a declaration.
 */
export interface LineInput {
  /**
   * Customs value in US dollars: the transaction value declared, not a retail price. Unset: the
   * duty rate is given, and an amount only where the duty does not depend on the value.
   */
  customs_value?: number | string | null;
  /**
   * Answers to the questions of the facts catalogue (GET /v2/facts), by name. A name outside
   * the catalogue is said in warnings and never used.
   */
  facts?: Record<string, number | string | boolean>;
  /**
   * The HTS code of the goods: 4, 6, 8 or 10 digits, dots and spaces ignored. A rate needs the
   * 10-digit statistical line or its 8-digit subheading.
   */
  hts: string;
  /**
   * Country of origin: where the goods were produced, not where they ship from. ISO 3166-1
   * alpha-2 (XK for Kosovo), or a code U.S. Customs files with (BU, GZ, KV, WE).
   */
  origin: string;
  /**
   * A trade agreement's symbol from the HTS special column (S for USMCA, KR for KORUS…; GET
   * /v2/agreements). Giving it declares that the goods meet its rules of origin and that you
   * hold the proof.
   */
  preference?: string | null;
  /**
   * Quantities in the units a duty counts (kg, l, item, dozen, pair, proof_liter…),
   * nonnegative. An answer names the quantity it needs in missing ("quantities.kg").
   */
  quantities?: Record<string, number | string>;
  /**
   * Your reference for the line.
   */
  reference?: string;
}

/**
 * What the service needs to give a figure.
 */
export interface MissingField {
  /**
   * The values a choice takes.
   */
  choices?: unknown[] | null;
  /**
   * Where to send it in the request.
   */
  field: string;
  /**
   * What it asks, in words.
   */
  question: string;
  /**
   * The type of its value: number, money, boolean, choice, text, heading, country or datetime.
   */
  type: string;
  /**
   * The unit of a quantity.
   */
  unit?: string | null;
}

/**
 * A saved estimate, with the detail behind its answer.
 */
export interface SavedDetail {
  /**
   * Who saved it.
   */
  author: string;
  /**
   * When it was saved.
   */
  created_at: string;
  /**
   * All the duties, in US dollars.
   */
  estimated_duty: string | null;
  /**
   * Its identifier.
   */
  id: string;
  /**
   * The incidents found since that concern it.
   */
  incidents: SavedIncident[];
  /**
   * The request as calculated: its date, publication and answers.
   */
  inputs: Record<string, unknown>;
  /**
   * single: one product. entry: a declaration.
   */
  kind: "single" | "entry";
  /**
   * The name it was given.
   */
  label: string;
  /**
   * The publication of the rules it was calculated with: send it as publication_id to calculate
   * again with the same rules.
   */
  publication_id: string | null;
  /**
   * Its answer and its detail.
   */
  result: AuditedEstimate | AuditedDeclaration;
  /**
   * Where it was saved: api, mcp, portal or import.
   */
  source: string;
  /**
   * calculated: every duty is established; without a customs value, a duty that does not need
   * it comes with estimated_fees and estimated_landed_cost null, and a warning says so.
   * rate_only: no customs value was sent, and estimated_duty_rate is the answer; send the value
   * for the amounts. needs_information: something is missing to give a figure, and missing says
   * what to send again, on each line of a declaration. partial: a duty is withheld for now, and
   * withheld says which; no total is given. unsupported: a regime or a rate the service does
   * not calculate. not_found: a code the tariff does not have, or that names no product.
   * not_covered: the date or the chapter is outside the data.
   */
  status: "calculated" | "rate_only" | "needs_information" | "partial" | "unsupported" | "not_found" | "not_covered";
}

/**
 * An incident found since an estimate was saved, that concerns it.
 */
export interface SavedIncident {
  /**
   * The duty calculated again once verified; null while it is being verified.
   */
  corrected_duty: string | null;
  /**
   * The entry fees calculated again once verified; null while it is being verified, or when
   * they were not asked.
   */
  corrected_fees: string | null;
  /**
   * What is being verified or was corrected, in words.
   */
  notice: string;
  /**
   * pending: being verified. wrong: confirmed wrong, the corrected figures say by how much.
   * unaffected: verified, the figures saved stand.
   */
  outcome: "pending" | "wrong" | "unaffected";
  /**
   * The incident, as the emails and the status page name it.
   */
  reference: string;
}

/**
 * A page of saved estimates, the newest first.
 */
export interface SavedList {
  /**
   * How many there are in all.
   */
  count: number;
  /**
   * How many were asked.
   */
  limit: number;
  /**
   * How many were skipped.
   */
  offset: number;
  /**
   * This page.
   */
  results: SavedSummary[];
}

/**
 * A saved estimate in a list.
 */
export interface SavedSummary {
  /**
   * Who saved it.
   */
  author: string;
  /**
   * When it was saved.
   */
  created_at: string;
  /**
   * All the duties, in US dollars.
   */
  estimated_duty: string | null;
  /**
   * Its identifier.
   */
  id: string;
  /**
   * The incidents found since that concern it.
   */
  incidents: SavedIncident[];
  /**
   * single: one product. entry: a declaration.
   */
  kind: "single" | "entry";
  /**
   * The name it was given.
   */
  label: string;
  /**
   * The publication of the rules it was calculated with: send it as publication_id to calculate
   * again with the same rules.
   */
  publication_id: string | null;
  /**
   * Where it was saved: api, mcp, portal or import.
   */
  source: string;
  /**
   * calculated: every duty is established; without a customs value, a duty that does not need
   * it comes with estimated_fees and estimated_landed_cost null, and a warning says so.
   * rate_only: no customs value was sent, and estimated_duty_rate is the answer; send the value
   * for the amounts. needs_information: something is missing to give a figure, and missing says
   * what to send again, on each line of a declaration. partial: a duty is withheld for now, and
   * withheld says which; no total is given. unsupported: a regime or a rate the service does
   * not calculate. not_found: a code the tariff does not have, or that names no product.
   * not_covered: the date or the chapter is outside the data.
   */
  status: "calculated" | "rate_only" | "needs_information" | "partial" | "unsupported" | "not_found" | "not_covered";
}

/**
 * The official document an amount rests on.
 */
export interface Source {
  /**
   * The SHA-256 of the file, to check it is the one cited.
   */
  sha256: string | null;
  /**
   * Its title.
   */
  title: string | null;
  /**
   * Where to read it: the file of that edition.
   */
  url: string | null;
}

/**
 * Whether the data can be relied on now, and which data answers. The pages /status/ and
 * /coverage/ say more.
 */
export interface Status {
  /**
   * When the official sources were last checked.
   */
  checked_at: string | null;
  /**
   * The first day an estimate can be dated.
   */
  covered_from: string | null;
  /**
   * The edition of the US tariff, in words.
   */
  edition: string | null;
  /**
   * The engine that calculates every estimate now.
   */
  engine_version: string;
  /**
   * The wrong rates being corrected.
   */
  incidents: StatusIncident[];
  /**
   * The publication of the rules in service. When it changes, or the engine does, an estimate
   * you kept may give another result.
   */
  publication_id: string | null;
  /**
   * True when those checks are older than they should be.
   */
  stale: boolean;
  /**
   * ok: the official sources were verified lately. degraded: they could not be: estimates still
   * answer, from the data last verified.
   */
  status: "ok" | "degraded";
}

/**
 * A wrong rate being corrected.
 */
export interface StatusIncident {
  /**
   * What is being corrected, in words.
   */
  notice: string;
  /**
   * When it was opened.
   */
  opened_at: string;
  /**
   * The incident, as the emails and the status page name it.
   */
  reference: string;
  /**
   * Where it stands: open, notified or corrected.
   */
  status: string;
}

/**
 * What the total leaves out for now.
 */
export interface Withheld {
  /**
   * Its Chapter 99 heading, if any.
   */
  heading: string | null;
  /**
   * What is withheld, in words.
   */
  name: string;
  /**
   * Why, and what it means for the total.
   */
  reason: string;
}

/**
 * What search_hts takes in its query.
 */
export interface SearchHtsQuery {
  /**
   * A code, or words of the descriptions: 200 characters at most.
   */
  q?: string;
  /**
   * Two digits, as 61: the lines of that chapter only.
   */
  chapter?: string;
  /**
   * How many lines to skip, from 0 to 100000.
   *
   * Default: 0.
   */
  offset?: number;
  /**
   * How many lines to return, from 1 to 100.
   *
   * Default: 50.
   */
  limit?: number;
}

/**
 * What list_saved_estimates takes in its query.
 */
export interface ListSavedEstimatesQuery {
  /**
   * How many saved estimates to skip.
   *
   * Default: 0.
   */
  offset?: number;
  /**
   * How many saved estimates to return, from 1 to 100.
   *
   * Default: 50.
   */
  limit?: number;
}
