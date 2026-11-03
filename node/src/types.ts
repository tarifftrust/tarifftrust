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
 * An item of a batch that could not be calculated; the others are.
 */
export interface BatchFailure {
  /**
   * Why it has no result: invalid_input with its fields, or no data for its date yet
   * (data_unavailable, edition_not_published): send it again later.
   */
  error: Error;
  /**
   * The item's position in items, from 0.
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
   * A formal entry pays the merchandise processing fee (MPF) on its value; an informal one, the
   * fixed informal fee.
   *
   * Default: "formal".
   */
  entry_type?: "formal" | "informal";
  /**
   * Answers to the questions of the facts catalogue (GET /v1/facts), by name. A name outside
   * the catalogue is reported in the result and never used.
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
   * Count the entry fees (MPF, HMF) of a declaration of this product alone; the landed cost
   * includes them only then. The MPF is charged once on a declaration: for several products
   * entered together, use POST /v1/estimates/entry.
   *
   * Default: false.
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
   * /v1/agreements). Giving it declares that the goods meet its rules of origin and that you
   * hold the proof.
   */
  preference?: string | null;
  /**
   * Quantities in the units a duty counts (kg, l, item, dozen, pair, proof_liter…),
   * nonnegative. A result names the quantity it needs in required_fields ("quantities.kg").
   */
  quantities?: Record<string, number | string>;
  /**
   * How the goods arrive; by sea they also pay the harbor maintenance fee (HMF). Unset: land
   * for goods of Canada or Mexico, ocean otherwise.
   */
  transport_mode?: "air" | "ocean" | "land" | null;
}

/**
 * Up to 200 products, each calculated on its own: POST /v1/estimates/batch.
 */
export interface BatchRequest {
  /**
   * The products, each calculated on its own.
   */
  items: BatchItem[];
  /**
   * Calculate with this publication of the rules rather than the one in force on the date: a
   * saved result's publication_id replays it.
   */
  publication_id?: string | null;
}

/**
 * The products of a batch, each calculated on its own.
 */
export interface BatchResult {
  /**
   * The freshness of each publication used, by its id.
   */
  freshness: Record<string, Freshness>;
  /**
   * The publication every item was calculated with; null when they differ (their dates do).
   */
  publication_id: string | null;
  /**
   * Every publication used.
   */
  publication_ids: string[];
  /**
   * One per item, in the order sent: its result, or its error.
   */
  results: (BatchSuccess | BatchFailure)[];
}

/**
 * An item of a batch that was calculated.
 */
export interface BatchSuccess {
  /**
   * The item's position in items, from 0.
   */
  index: number;
  /**
   * Its result, as POST /v1/estimates gives it, without last_approved.
   */
  result: CalculationResult;
}

/**
 * One product: the line, with the fees of its one-line declaration.
 */
export interface CalculationResult {
  /**
   * Measures whose relations do not settle (two caps on the same duties, contradictory
   * relations): the duties concerned stay unresolved, and estimated_duty is null.
   */
  alerts?: string[];
  /**
   * The facts the request answered, each with the measures it decides (those whose decision
   * another answer would change); none when, given the other answers, it decides nothing.
   */
  answers?: Record<string, unknown>[];
  /**
   * The legal day the duties are calculated for, in New York time.
   */
  as_of: string;
  /**
   * Instant of effect (New York time) when a transition on that day depends on the hour.
   */
  as_of_instant?: string | null;
  /**
   * The answers this estimate assumed because none was declared (the ordinary case): for each,
   * the fact, the value assumed, its question, its type and choices, and under alternatives
   * what each other answer would give. Send your own answer in facts to replace one.
   */
  assumptions?: Record<string, unknown>[];
  /**
   * The base rate as the tariff prints it, in the column read: general, special (an agreement
   * claimed and granted) or column 2.
   */
  base_rate: string | null;
  /**
   * With a shorter code: the 8- and 10-digit lines under it, up to 25.
   */
  candidates?: Candidate[] | null;
  /**
   * The line's three rate columns as printed: general, special and other (column 2).
   */
  column_rates?: Record<string, string> | null;
  /**
   * The duties counted, the base duty first, each with its amount and its source.
   */
  components: Component[];
  /**
   * Always USD: every amount is in US dollars.
   */
  currency: "USD";
  /**
   * The line's descriptions, from the heading down.
   */
  description?: string | null;
  /**
   * The duty as a share of the customs value, for comparison.
   */
  duty_rate?: DutyRate | null;
  /**
   * The version of the engine that calculated it.
   */
  engine_version: string;
  /**
   * What the estimate covers, in words: implemented measures only, unknown never zero.
   */
  estimate_scope: string;
  /**
   * Implemented measures only. Null means unknown, never zero: information is missing, a
   * position is in review or an incident suspends it.
   */
  estimated_duty: string | null;
  /**
   * Customs value + estimated duty + freight + insurance, and the entry fees only when
   * include_fees was asked. Null while the duty, an asked fee or the value is unknown.
   */
  estimated_landed_cost: string | null;
  /**
   * Decision, reason and source of every measure examined for this case.
   */
  examined_measures?: ExaminedMeasure[];
  /**
   * The entry fees asked (include_fees), for a declaration of this product.
   */
  fees: Fee[];
  /**
   * not_requested: include_fees is false. estimated: every fee owed is known. partial: one is
   * not (a value is missing, or the date or entry type has no fee schedule). not_covered: an
   * entry regime outside the service, no fee calculated. include_fees is false by default for
   * one product.
   */
  fees_status: "not_requested" | "not_covered" | "estimated" | "partial";
  /**
   * The tariff's footnotes for the line, which may impose conditions.
   */
  footnotes?: unknown[] | null;
  /**
   * Whether the sources were verified recently enough.
   */
  freshness?: Freshness | null;
  /**
   * The HTS code calculated, in digits.
   */
  hts: string;
  /**
   * One question per missing input, to ask before calculating again.
   */
  input_guidance?: InputGuidance[] | null;
  /**
   * When the publication was prepared: the state of knowledge the result rests on.
   */
  knowledge_at: string | null;
  /**
   * Sum of the components whose validity is established; null when none is.
   */
  known_duty_subtotal: string | null;
  /**
   * Sum of the fees established in fees; null when fees is empty (not asked, or no fee
   * established for this date, entry type or regime).
   */
  known_fee_subtotal?: string | null;
  /**
   * In a history: the IEEPA duties established at that point; 0.00 when none applies, from
   * 2026-02-24; null otherwise.
   */
  known_ieepa_subtotal?: string | null;
  /**
   * When positions in review or incidents withhold part of the result: the last result
   * established without them, dated. Historical only: never part of a subtotal, total or
   * exposure. Absent from batch items.
   */
  last_approved?: LastApproved | null;
  /**
   * How the code was found in the tariff.
   */
  match: Match;
  /**
   * The country of origin, as sent.
   */
  origin: string;
  /**
   * The workspace's standing answers applied, each marked when the request overrode it.
   */
  policies?: Record<string, unknown>[];
  /**
   * What identifies this result for a replay: the engine result's checksum, the request as the
   * engine read it, the legal end of its publication and the image of the engine.
   */
  provenance?: Record<string, unknown> | null;
  /**
   * The checksum of that publication's files.
   */
  publication_checksum: string | null;
  /**
   * The publication of the rules it was calculated with: send it as publication_id to calculate
   * again with the same rules.
   */
  publication_id: string;
  /**
   * The edition of the US tariff, in words.
   */
  publication_label: string;
  /**
   * Your reference for the line, as sent.
   */
  reference?: string | null;
  /**
   * When a measure replaces the base duty: the base duty replaced, with the reason; in no
   * total.
   */
  replaced_base?: Record<string, unknown> | null;
  /**
   * The inputs still missing, each asked in input_guidance.
   */
  required_fields: string[];
  /**
   * Shown apart, subject to a position in review; in no total.
   */
  reserved_components?: Component[];
  /**
   * What withholds part of the estimate: a position in review (position), a wrong-rate incident
   * (incident), an official notice not yet read (notice), a measure in force whose rate is not
   * announced yet (pending_rate).
   */
  review_pending?: ReviewPending[];
  /**
   * With unanswered yes/no or choice facts that have no ordinary case, every coherent
   * combination of their answers (up to twelve) and exact bounds; beyond, a prudent range. Null
   * otherwise.
   */
  scenarios?: Scenarios | null;
  /**
   * Every official document the result rests on.
   */
  sources: Source[];
  /**
   * The statistical units the tariff prints for the line (No., kg).
   */
  statistical_units?: string[] | null;
  /**
   * What the answer is, to read before its amounts. calculated: every component is established.
   * needs_information: what you can give is missing (a fact, a quantity, the value, a more
   * precise code or the instant of effect), asked in input_guidance. partial: a component stays
   * unknown that you cannot give (a position in review, an incident, incomplete coverage),
   * listed in review_pending. unsupported: a rate, a formula or an entry regime the engine does
   * not calculate. not_covered: a date or a chapter outside the data, or a code of chapters 98
   * and 99, which needs the product's own code. not_found: no such code in the tariff, nor any
   * more precise one.
   */
  status: "calculated" | "partial" | "needs_information" | "unsupported" | "not_found" | "not_covered";
  /**
   * The entry fees (MPF, HMF) of a declaration of this product alone, when include_fees was
   * asked; null when they were not asked, or while one of them is not established.
   */
  total_fees: string | null;
  /**
   * Whether the scheduled verification of the sources works; separate from freshness.
   */
  verification?: Verification | null;
  /**
   * Cautions in words, to show with the result: a preference declared, footnotes, fees not
   * established, sources not verified recently.
   */
  warnings: string[];
}

/**
 * A line of the tariff under a code too short to calculate.
 */
export interface Candidate {
  /**
   * Its description.
   */
  description: string;
  /**
   * A line under the code sent, of 8 or 10 digits.
   */
  hts: string;
}

/**
 * One duty counted in the result: the base duty, a Chapter 99 measure, or a cap's deduction.
 */
export interface Component {
  /**
   * The duty in dollars; null when unknown (an input is missing, or the rate is not calculated
   * or not announced yet). Negative for a cap's deduction.
   */
  amount: string | null;
  /**
   * The base rate as the tariff prints it; null for a measure, whose rate is in terms.
   */
  expression?: string | null;
  /**
   * The measure's Chapter 99 heading; null for the base duty.
   */
  heading?: string | null;
  /**
   * base_rate for the base duty; otherwise the identifier of the measure.
   */
  id: string;
  /**
   * The duty in words: Base duty, Column 2, or the measure's title.
   */
  label: string;
  /**
   * base for the base duty; otherwise the measure's program, as 301, 232, 201 or 338.
   */
  program: string;
  /**
   * The inputs its amount still needs: customs_value, quantities.<unit>, facts.<name>.
   */
  required_fields: string[];
  /**
   * cap for a ceiling's deduction: what exceeds the ceiling, taken off the duties it limits.
   * Absent otherwise.
   */
  role?: string | null;
  /**
   * The identifier of the rule the measure comes from. Null for the base duty.
   */
  rule?: string | null;
  /**
   * The version of that rule.
   */
  rule_version?: string | null;
  /**
   * The official document of this rate.
   */
  source: Source;
  /**
   * calculated: the amount is established. needs_information: an input is missing, named in
   * required_fields. unsupported: a rate the engine does not calculate. pending: in force at a
   * rate the official text has not announced yet.
   */
  status: "calculated" | "needs_information" | "unsupported" | "pending";
  /**
   * The rate as typed terms, added together; null when the printed rate cannot be read.
   */
  terms: RateTerm[] | null;
  /**
   * May still be removed by an unanswered question: shown, but not in known_duty_subtotal.
   */
  uncertain?: boolean | null;
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
 * The duty as a share of the customs value, for comparison: implemented duties only, without
 * the fees and AD/CVD.
 */
export interface DutyRate {
  /**
   * What the rate is, in words.
   */
  basis?: string | null;
  /**
   * The duty as a decimal fraction of the customs value (0.415 for 41.5%).
   */
  estimated_ad_valorem_rate?: string | null;
  /**
   * complete: the result is calculated and every duty is a share of the value. estimated: the
   * share of the duties known, the result not settled. needs_information: an input other than
   * the value is missing. not_representable: a duty is no share of the value (per unit, capped
   * or undecided). unsupported: a rate the engine does not read. not_covered: no rate is read.
   */
  status: "not_covered" | "needs_information" | "unsupported" | "not_representable" | "estimated" | "complete";
  /**
   * The same, given only when the status is complete.
   */
  total_ad_valorem_rate?: string | null;
}

/**
 * A whole import declaration: every line, then the MPF and the HMF once on the declaration.
 * POST /v1/estimates/entry.
 */
export interface EntryInput {
  /**
   * When the goods are entered for consumption. A day, in New York time ("2026-04-05"); or, on
   * a day when a measure takes effect at a stated hour, the instant of entry with its UTC
   * offset ("2026-04-05T00:01:00-04:00"). Unset: today.
   */
  as_of?: string | null;
  /**
   * A formal entry pays the merchandise processing fee (MPF) on its value; an informal one, the
   * fixed informal fee.
   *
   * Default: "formal".
   */
  entry_type?: "formal" | "informal";
  /**
   * Answers that hold for the whole declaration (GET /v1/facts, scope entry or shipment).
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
   * The lines of the declaration, each a product.
   */
  lines: LineInput[];
  /**
   * Calculate with this publication of the rules rather than the one in force on the date: a
   * saved result's publication_id replays it.
   */
  publication_id?: string | null;
  /**
   * Your reference for the declaration.
   */
  reference?: string;
  /**
   * How the goods arrive; by sea they also pay the harbor maintenance fee (HMF). Unset: land
   * for goods of Canada or Mexico, ocean otherwise.
   */
  transport_mode?: "air" | "ocean" | "land" | null;
}

/**
 * A whole declaration: its lines, then its fees, once.
 */
export interface EntryResult {
  /**
   * The legal day of the declaration, in New York time.
   */
  as_of: string;
  /**
   * Instant of effect (New York time) when a transition on that day depends on the hour.
   */
  as_of_instant?: string | null;
  /**
   * Always USD: every amount is in US dollars.
   */
  currency?: "USD" | null;
  /**
   * The version of the engine that calculated it.
   */
  engine_version?: string | null;
  /**
   * formal or informal, as sent.
   */
  entry_type?: string | null;
  /**
   * What the estimate covers, in words: implemented measures only, unknown never zero.
   */
  estimate_scope?: string | null;
  /**
   * The duty of the declaration; null unless every line's is known. Unknown is never zero.
   */
  estimated_duty: string | null;
  /**
   * Customs values + estimated duty + freight + insurance, and the entry fees when include_fees
   * (true by default for a declaration). Null while the duty, an asked fee or a value is
   * unknown.
   */
  estimated_landed_cost: string | null;
  /**
   * MPF and HMF, once for the declaration.
   */
  fees: Fee[];
  /**
   * not_requested: include_fees is false. estimated: every fee owed is known. partial: one is
   * not (a value is missing, or the date or entry type has no fee schedule). not_covered: an
   * entry regime outside the service, no fee calculated. include_fees is true by default for a
   * declaration.
   */
  fees_status: "not_requested" | "not_covered" | "estimated" | "partial";
  /**
   * Whether the sources were verified recently enough.
   */
  freshness?: Freshness | null;
  /**
   * Empty: each line asks its own questions, in lines.
   */
  input_guidance?: InputGuidance[] | null;
  /**
   * Always entry.
   */
  kind: "entry";
  /**
   * When the publication was prepared: the state of knowledge the result rests on.
   */
  knowledge_at?: string | null;
  /**
   * Sum of the lines' established subtotals; null when none is.
   */
  known_duty_subtotal: string | null;
  /**
   * When positions in review or incidents withhold part of the result: the last result
   * established without them, dated. Historical only: never part of a subtotal, total or
   * exposure. Absent from batch items.
   */
  last_approved?: LastApproved | null;
  /**
   * Each line's result, in the order sent.
   */
  lines: LineResult[];
  /**
   * The workspace's standing answers applied, each marked when the request overrode it.
   */
  policies?: Record<string, unknown>[];
  /**
   * What identifies this result for a replay: the engine result's checksum, the request as the
   * engine read it, the legal end of its publication and the image of the engine.
   */
  provenance?: Record<string, unknown> | null;
  /**
   * The checksum of that publication's files.
   */
  publication_checksum?: string | null;
  /**
   * The publication of the rules it was calculated with: send it as publication_id to calculate
   * again with the same rules.
   */
  publication_id: string;
  /**
   * The edition of the US tariff, in words.
   */
  publication_label?: string | null;
  /**
   * Your reference for the declaration, as sent.
   */
  reference?: string | null;
  /**
   * Empty: each line names its own, in lines.
   */
  required_fields: string[];
  /**
   * With unanswered yes/no or choice facts that have no ordinary case, every coherent
   * combination of their answers (up to twelve) and exact bounds; beyond, a prudent range. Null
   * otherwise.
   */
  scenarios: Scenarios | null;
  /**
   * The status of the declaration: that of its least settled line.
   */
  status: "calculated" | "partial" | "needs_information" | "unsupported" | "not_found" | "not_covered";
  /**
   * The entry fees (MPF, HMF) of the declaration, counted once; null when include_fees is
   * false, or while one of them is not established.
   */
  total_fees: string | null;
  /**
   * The transport mode, as sent or inferred.
   */
  transport_mode?: string | null;
  /**
   * Whether the scheduled verification of the sources works; separate from freshness.
   */
  verification?: Verification | null;
  /**
   * Cautions on the declaration: its fees, the freshness and verification of the sources; each
   * line has its own.
   */
  warnings: string[];
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
 * One product at a date: POST /v1/estimates.
 */
export interface EstimateInput {
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
   * A formal entry pays the merchandise processing fee (MPF) on its value; an informal one, the
   * fixed informal fee.
   *
   * Default: "formal".
   */
  entry_type?: "formal" | "informal";
  /**
   * Answers to the questions of the facts catalogue (GET /v1/facts), by name. A name outside
   * the catalogue is reported in the result and never used.
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
   * Count the entry fees (MPF, HMF) of a declaration of this product alone; the landed cost
   * includes them only then. The MPF is charged once on a declaration: for several products
   * entered together, use POST /v1/estimates/entry.
   *
   * Default: false.
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
   * /v1/agreements). Giving it declares that the goods meet its rules of origin and that you
   * hold the proof.
   */
  preference?: string | null;
  /**
   * Calculate with this publication of the rules rather than the one in force on the date: a
   * saved result's publication_id replays it.
   */
  publication_id?: string | null;
  /**
   * Quantities in the units a duty counts (kg, l, item, dozen, pair, proof_liter…),
   * nonnegative. A result names the quantity it needs in required_fields ("quantities.kg").
   */
  quantities?: Record<string, number | string>;
  /**
   * How the goods arrive; by sea they also pay the harbor maintenance fee (HMF). Unset: land
   * for goods of Canada or Mexico, ocean otherwise.
   */
  transport_mode?: "air" | "ocean" | "land" | null;
}

/**
 * The decision on every Chapter 99 measure examined for this case.
 */
export interface ExaminedMeasure {
  /**
   * applied: its conditions hold. excluded: one fails, or another measure removes it.
   * undetermined: an unanswered question decides.
   */
  decision: "applied" | "excluded" | "undetermined";
  /**
   * The facts its conditions read: the questions this measure decides.
   */
  facts?: string[];
  /**
   * Its Chapter 99 heading.
   */
  heading: string;
  /**
   * Its title.
   */
  label: string;
  /**
   * The identifier of the measure.
   */
  measure: string;
  /**
   * Its program, as 301, 232, 201 or 338.
   */
  program: string;
  /**
   * Why, in words: the condition that decided, or what removed it.
   */
  reason: string;
  /**
   * The identifier of the rule the measure comes from.
   */
  rule: string;
  /**
   * The version of that rule.
   */
  rule_version: string | null;
  /**
   * The official document of the measure.
   */
  source: Source;
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
   * The ordinary case, assumed when unanswered and said in assumptions.
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
 * An entry fee, once for the declaration.
 */
export interface Fee {
  /**
   * The fee in dollars; null when unknown.
   */
  amount: string | null;
  /**
   * The exemption it rests on, if any: declared, or that of goods originating under the
   * agreement claimed.
   */
  assumption?: string | null;
  /**
   * The value it is calculated on: the customs values of the lines subject to it; null when one
   * is missing.
   */
  basis?: string | null;
  /**
   * MPF (merchandise processing fee) or HMF (harbor maintenance fee).
   */
  label: string;
  /**
   * The official fee schedule.
   */
  source: Source;
}

/**
 * How recently the official sources were verified.
 */
export interface Freshness {
  /**
   * Hours since then.
   */
  age_hours: number | null;
  /**
   * The verification schedule and its target, or why a past edition has none.
   */
  basis: string;
  /**
   * When the official sources were last verified successfully (before any verification, when
   * the edition was observed); null for a past edition.
   */
  checked_at: string | null;
  /**
   * True past the freshness target: the sources may have changed since.
   */
  stale: boolean;
}

/**
 * One product at every change of the US tariff over a period: POST /v1/estimates/history.
 */
export interface HistoryRequest {
  /**
   * Customs value in US dollars: the transaction value declared, not a retail price. Unset: the
   * duty rate is given, and an amount only where the duty does not depend on the value.
   */
  customs_value?: number | string | null;
  /**
   * A formal entry pays the merchandise processing fee (MPF) on its value; an informal one, the
   * fixed informal fee.
   *
   * Default: "formal".
   */
  entry_type?: "formal" | "informal";
  /**
   * Answers to the questions of the facts catalogue (GET /v1/facts), by name. A name outside
   * the catalogue is reported in the result and never used.
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
   * Count the entry fees (MPF, HMF) of a declaration of this product alone; the landed cost
   * includes them only then. The MPF is charged once on a declaration: for several products
   * entered together, use POST /v1/estimates/entry.
   *
   * Default: false.
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
   * /v1/agreements). Giving it declares that the goods meet its rules of origin and that you
   * hold the proof.
   */
  preference?: string | null;
  /**
   * Quantities in the units a duty counts (kg, l, item, dozen, pair, proof_liter…),
   * nonnegative. A result names the quantity it needs in required_fields ("quantities.kg").
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
 * One product at every change of the tariff over a period.
 */
export interface HistoryResult {
  /**
   * How the points are calculated, in words.
   */
  basis: string;
  /**
   * The periods the service holds rules for within the period asked: no point lies outside.
   */
  covered_windows: CoveredWindow[];
  /**
   * One result per change of the tariff, in date order, each on its as_of.
   */
  points: CalculationResult[];
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
 * One question for a missing input, to ask before calculating again.
 */
export interface InputGuidance {
  /**
   * The values to choose from, for a choice.
   */
  choices?: unknown[] | null;
  /**
   * Why it is asked, or how to answer it.
   */
  description: string;
  /**
   * Where to send the answer, as required_fields names it: facts.<name>, quantities.<unit>,
   * customs_value, preference, hts or as_of.
   */
  field: string;
  /**
   * observable or choice (a fact of the goods), declared_conclusion (a conclusion you declare,
   * as whether a Chapter 99 heading applies) or input (a plain input).
   */
  kind?: string | null;
  /**
   * The question in a few words.
   */
  label: string;
  /**
   * The text the question comes from.
   */
  legal_basis?: string | null;
  /**
   * The question to ask.
   */
  question?: string | null;
  /**
   * product: the line's own; entry or shipment: the whole declaration's.
   */
  scope?: string | null;
  /**
   * How it is answered: boolean, choice, money, number, country, heading, text or datetime.
   */
  type: string;
  /**
   * The unit of a number, if any.
   */
  unit?: string | null;
}

/**
 * The last result established without the items now withheld: historical, in no total.
 */
export interface LastApproved {
  /**
   * When that publication was approved.
   */
  approved_from?: string | null;
  /**
   * Until when it was approved; null while it still is.
   */
  approved_to?: string | null;
  /**
   * Legal date of this result; the edition's last day for an older edition.
   */
  as_of: string;
  /**
   * The edition of the US tariff, in words.
   */
  edition: string;
  /**
   * The duty of that result.
   */
  estimated_duty: string | null;
  /**
   * The landed cost of that result.
   */
  estimated_landed_cost?: string | null;
  /**
   * The established subtotal of that result.
   */
  known_duty_subtotal: string | null;
  /**
   * The publication it was calculated with.
   */
  publication_id: string;
  /**
   * The status of that result.
   */
  status: string;
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
   * Answers to the questions of the facts catalogue (GET /v1/facts), by name. A name outside
   * the catalogue is reported in the result and never used.
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
   * /v1/agreements). Giving it declares that the goods meet its rules of origin and that you
   * hold the proof.
   */
  preference?: string | null;
  /**
   * Quantities in the units a duty counts (kg, l, item, dozen, pair, proof_liter…),
   * nonnegative. A result names the quantity it needs in required_fields ("quantities.kg").
   */
  quantities?: Record<string, number | string>;
  /**
   * Your reference for the line.
   */
  reference?: string;
}

/**
 * One line of a declaration: its duties. The fees and the landed cost are those of the
 * declaration, calculated once for all its lines.
 */
export interface LineResult {
  /**
   * Measures whose relations do not settle (two caps on the same duties, contradictory
   * relations): the duties concerned stay unresolved, and estimated_duty is null.
   */
  alerts?: string[];
  /**
   * The facts the request answered, each with the measures it decides (those whose decision
   * another answer would change); none when, given the other answers, it decides nothing.
   */
  answers?: Record<string, unknown>[];
  /**
   * The legal day the duties are calculated for, in New York time.
   */
  as_of: string;
  /**
   * Instant of effect (New York time) when a transition on that day depends on the hour.
   */
  as_of_instant?: string | null;
  /**
   * The answers this estimate assumed because none was declared (the ordinary case): for each,
   * the fact, the value assumed, its question, its type and choices, and under alternatives
   * what each other answer would give. Send your own answer in facts to replace one.
   */
  assumptions?: Record<string, unknown>[];
  /**
   * The base rate as the tariff prints it, in the column read: general, special (an agreement
   * claimed and granted) or column 2.
   */
  base_rate: string | null;
  /**
   * With a shorter code: the 8- and 10-digit lines under it, up to 25.
   */
  candidates?: Candidate[] | null;
  /**
   * The line's three rate columns as printed: general, special and other (column 2).
   */
  column_rates?: Record<string, string> | null;
  /**
   * The duties counted, the base duty first, each with its amount and its source.
   */
  components: Component[];
  /**
   * Always USD: every amount is in US dollars.
   */
  currency: "USD";
  /**
   * The line's descriptions, from the heading down.
   */
  description?: string | null;
  /**
   * The duty as a share of the customs value, for comparison.
   */
  duty_rate?: DutyRate | null;
  /**
   * The version of the engine that calculated it.
   */
  engine_version: string;
  /**
   * What the estimate covers, in words: implemented measures only, unknown never zero.
   */
  estimate_scope: string;
  /**
   * Implemented measures only. Null means unknown, never zero: information is missing, a
   * position is in review or an incident suspends it.
   */
  estimated_duty: string | null;
  /**
   * Decision, reason and source of every measure examined for this case.
   */
  examined_measures?: ExaminedMeasure[];
  /**
   * The tariff's footnotes for the line, which may impose conditions.
   */
  footnotes?: unknown[] | null;
  /**
   * The HTS code calculated, in digits.
   */
  hts: string;
  /**
   * One question per missing input, to ask before calculating again.
   */
  input_guidance?: InputGuidance[] | null;
  /**
   * When the publication was prepared: the state of knowledge the result rests on.
   */
  knowledge_at: string | null;
  /**
   * Sum of the components whose validity is established; null when none is.
   */
  known_duty_subtotal: string | null;
  /**
   * How the code was found in the tariff.
   */
  match: Match;
  /**
   * The country of origin, as sent.
   */
  origin: string;
  /**
   * The checksum of that publication's files.
   */
  publication_checksum: string | null;
  /**
   * The publication of the rules it was calculated with: send it as publication_id to calculate
   * again with the same rules.
   */
  publication_id: string;
  /**
   * The edition of the US tariff, in words.
   */
  publication_label: string;
  /**
   * Your reference for the line, as sent.
   */
  reference?: string | null;
  /**
   * When a measure replaces the base duty: the base duty replaced, with the reason; in no
   * total.
   */
  replaced_base?: Record<string, unknown> | null;
  /**
   * The inputs still missing, each asked in input_guidance.
   */
  required_fields: string[];
  /**
   * Shown apart, subject to a position in review; in no total.
   */
  reserved_components?: Component[];
  /**
   * What withholds part of the estimate: a position in review (position), a wrong-rate incident
   * (incident), an official notice not yet read (notice), a measure in force whose rate is not
   * announced yet (pending_rate).
   */
  review_pending?: ReviewPending[];
  /**
   * Every official document the result rests on.
   */
  sources: Source[];
  /**
   * The statistical units the tariff prints for the line (No., kg).
   */
  statistical_units?: string[] | null;
  /**
   * What the answer is, to read before its amounts. calculated: every component is established.
   * needs_information: what you can give is missing (a fact, a quantity, the value, a more
   * precise code or the instant of effect), asked in input_guidance. partial: a component stays
   * unknown that you cannot give (a position in review, an incident, incomplete coverage),
   * listed in review_pending. unsupported: a rate, a formula or an entry regime the engine does
   * not calculate. not_covered: a date or a chapter outside the data, or a code of chapters 98
   * and 99, which needs the product's own code. not_found: no such code in the tariff, nor any
   * more precise one.
   */
  status: "calculated" | "partial" | "needs_information" | "unsupported" | "not_found" | "not_covered";
  /**
   * Cautions in words, to show with the result: a preference declared, footnotes, fees not
   * established, sources not verified recently.
   */
  warnings: string[];
}

/**
 * How the code sent was found in the tariff.
 */
export interface Match {
  /**
   * The number of digits of the code sent.
   */
  level: number;
  /**
   * The line found.
   */
  matched_hts?: string | null;
  /**
   * direct: the line's own rates. parent: a 10-digit line without rates of its own takes those
   * of its 8-digit line.
   */
  rate_basis: "direct" | "parent" | null;
  /**
   * The line whose rates are read.
   */
  rate_hts?: string | null;
  /**
   * exact: a line of the tariff. prefix_candidates: a shorter code, the lines under it in
   * candidates. none: not found, or not calculated (a date or chapter not covered).
   */
  type: "none" | "exact" | "prefix_candidates";
}

/**
 * One term of a rate; the terms of a rate are added together.
 */
export interface RateTerm {
  /**
   * Dollars per unit, for a specific term.
   */
  amount?: string | null;
  /**
   * For a top_up, the duty it completes: applicable (the line's base duty) or mfn (the column 1
   * general duty).
   */
  basis?: string | null;
  /**
   * The fact that gives the value the term applies to: the part's value (content), or the value
   * a top_up covers.
   */
  field?: string | null;
  /**
   * The form of the term. ad_valorem: a share of the value. specific: an amount per unit.
   * content: a share of the value of a part (a watch's movement). top_up: what brings the duty
   * up to a share of the value. sugar: the polarization formula. named: a calculator of the
   * engine. pending: announced without its rate.
   */
  kind: "ad_valorem" | "content" | "named" | "pending" | "specific" | "sugar" | "top_up";
  /**
   * A decimal fraction (0.165 for 16.5%): of the value (ad_valorem), of the part's value
   * (content), the share a top_up brings the duty to, or the sugar formula's rate per kilogram.
   */
  rate?: string | null;
  /**
   * The unit a specific term counts, as in quantities (kg, l, item…).
   */
  unit?: string | null;
}

/**
 * What withholds part of an estimate.
 */
export interface ReviewPending {
  /**
   * When it was detected.
   */
  detected_at?: string | null;
  /**
   * What it may do to the estimate: additional (a duty on top of the others), may_modify
   * (change the duties it names, which are withheld), none, or unknown (change any duty: all
   * are withheld).
   */
  effect: string;
  /**
   * position: a Chapter 99 position in review. incident: an open wrong-rate incident. notice:
   * an official notice not yet read. pending_rate: a measure in force whose rate is not
   * announced yet.
   */
  kind: "position" | "incident" | "notice" | "pending_rate";
  /**
   * The Chapter 99 heading concerned, if any.
   */
  position?: string | null;
  /**
   * Why the estimate is withheld, in words.
   */
  reason: string;
  /**
   * The incident's or the notice's reference.
   */
  reference?: string | null;
}

/**
 * Calculate and save one product (estimate) or a declaration (entry): exactly one.
 */
export interface SaveRequest {
  /**
   * A declaration to calculate and save, instead of estimate.
   */
  entry?: EntryInput | null;
  /**
   * One product to calculate and save. Give estimate or entry, not both.
   */
  estimate?: EstimateInput | null;
  /**
   * A name for the saved estimate.
   */
  label?: string;
}

/**
 * An estimate just calculated and saved.
 */
export interface Saved {
  /**
   * For a declaration: the declaration it is saved as in the portal.
   */
  entry_id?: string | null;
  /**
   * The saved estimate's identifier.
   */
  id: string;
  /**
   * single: one product. entry: a declaration.
   */
  kind: "single" | "entry";
  /**
   * Its result, as POST /v1/estimates or POST /v1/estimates/entry gives it.
   */
  result: CalculationResult | EntryResult;
}

/**
 * A saved estimate with its request and its result, as they were.
 */
export interface SavedDetail {
  /**
   * Who saved it: the API key, by its name, or the person.
   */
  author: string;
  /**
   * When it was saved.
   */
  created_at: string;
  /**
   * The version of the engine that calculated it.
   */
  engine_version: string;
  /**
   * The duty of its result, as it was calculated.
   */
  estimated_duty: string | null;
  /**
   * Its identifier: read it with GET /v1/saved-estimates/{id}.
   */
  id: string;
  /**
   * The image of the engine that replays it exactly.
   */
  image_digest: string | null;
  /**
   * The incidents found since it was saved that concern it, the oldest first; empty when there
   * are none.
   */
  incidents: SavedIncident[];
  /**
   * The request, in the fields of the API: an EstimateInput (single) or an EntryInput (entry).
   */
  inputs: Record<string, unknown>;
  /**
   * single: one product. entry: a declaration.
   */
  kind: "single" | "entry";
  /**
   * Its name, as given when saved.
   */
  label: string;
  /**
   * The publication it was calculated with.
   */
  publication_id: string | null;
  /**
   * The result as its engine_version calculated it, never recalculated: a CalculationResult
   * (single) or an EntryResult (entry) of that version.
   */
  result: Record<string, unknown>;
  /**
   * Where it was saved: api, mcp, portal, import (a declaration imported in the portal) or
   * report (the case of an error report).
   */
  source: string;
  /**
   * The status of its result, as it was calculated: incidents says what was found since.
   */
  status: string | null;
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
 * A page of the workspace's saved estimates.
 */
export interface SavedList {
  /**
   * How many saved estimates the workspace has.
   */
  count: number;
  /**
   * How many a page holds, as asked.
   */
  limit: number;
  /**
   * How many were skipped, as asked.
   */
  offset: number;
  /**
   * This page, the latest first.
   */
  results: SavedSummary[];
}

/**
 * A saved estimate, as the list gives it.
 */
export interface SavedSummary {
  /**
   * Who saved it: the API key, by its name, or the person.
   */
  author: string;
  /**
   * When it was saved.
   */
  created_at: string;
  /**
   * The version of the engine that calculated it.
   */
  engine_version: string;
  /**
   * The duty of its result, as it was calculated.
   */
  estimated_duty: string | null;
  /**
   * Its identifier: read it with GET /v1/saved-estimates/{id}.
   */
  id: string;
  /**
   * The image of the engine that replays it exactly.
   */
  image_digest: string | null;
  /**
   * The incidents found since it was saved that concern it, the oldest first; empty when there
   * are none.
   */
  incidents: SavedIncident[];
  /**
   * single: one product. entry: a declaration.
   */
  kind: "single" | "entry";
  /**
   * Its name, as given when saved.
   */
  label: string;
  /**
   * The publication it was calculated with.
   */
  publication_id: string | null;
  /**
   * Where it was saved: api, mcp, portal, import (a declaration imported in the portal) or
   * report (the case of an error report).
   */
  source: string;
  /**
   * The status of its result, as it was calculated: incidents says what was found since.
   */
  status: string | null;
}

/**
 * One combination of answers to the questions left open, and what it gives.
 */
export interface Scenario {
  /**
   * One answer to each question: its fact, its line (from 0; null for a question of the whole
   * declaration) and its value.
   */
  answers: Record<string, unknown>[];
  /**
   * The duty with these answers.
   */
  estimated_duty: string | null;
  /**
   * Duty and fees with these answers; null when one is unknown.
   */
  estimated_total: string | null;
  /**
   * The fees with these answers; null when not asked or unknown.
   */
  total_fees: string | null;
}

/**
 * What the estimate would be under each answer to the questions that have no ordinary case.
 */
export interface Scenarios {
  /**
   * minimum and maximum of estimated_total, with their label; null when a combination has no
   * total.
   */
  bounds: Record<string, string> | null;
  /**
   * The questions the scenarios answer.
   */
  facts: string[];
  /**
   * exact: every combination calculated. prudent: more than twelve, bounds only.
   */
  kind: "exact" | "prudent";
  /**
   * Each combination; empty for a prudent range.
   */
  scenarios: Scenario[];
}

/**
 * An official document a rate, a measure or a fee is read from.
 */
export interface Source {
  /**
   * True when the duty rests on an official notice (a proclamation, a USTR notice, a customs
   * message) that the USITC tariff does not hold yet.
   */
  ahead_of_tariff?: boolean | null;
  /**
   * Who publishes it: USITC, CBP, USTR, the Federal Register…
   */
  authority: string;
  /**
   * The same SHA-256 as sha256, under the name some sources give it.
   */
  checksum?: string | null;
  /**
   * SHA-256 of the document as archived: the very copy the rate was read from.
   */
  sha256?: string | null;
  /**
   * Its title, or the edition of the tariff. A measure whose text has not changed since keeps
   * citing an earlier edition than the publication's.
   */
  title?: string | null;
  /**
   * Where the official document is published: an edition of the tariff at its own file, which
   * keeps serving the bytes of sha256. A publication prepared before 2026-11-03 gives the
   * address of the current edition instead, whose bytes differ once a later edition is out.
   */
  url?: string | null;
}

/**
 * Freshness and verification of the data, and its coverage; the same as the pages /status/ and
 * /coverage/.
 */
export interface Status {
  /**
   * Chapter 99 positions and their status, the share of estimates withheld, historical periods,
   * base rates, agreements, fees and what is out of scope.
   */
  coverage: Record<string, unknown>;
  /**
   * The engine that calculates every estimate now.
   */
  engine_version: string;
  /**
   * Past this age, the sources are stale.
   */
  freshness_target_hours: number;
  /**
   * True while no new publication may be put in service.
   */
  frozen: boolean;
  /**
   * Wrong-rate incidents open, notified or corrected: reference, status, notice and opened_at.
   */
  incidents: Record<string, unknown>[];
  /**
   * Positions still in review after the public notice delay: position, since, reason and
   * detected_at.
   */
  notices: Record<string, unknown>[];
  /**
   * The publications in service, by edition: edition, valid_from, valid_to, publication_id and
   * approved_from.
   */
  publications: Record<string, unknown>[];
  /**
   * Until when the fee schedules run (fee_rules_until), and in how many days (days_remaining).
   */
  rule_horizon: Record<string, unknown>;
  /**
   * Whether the scheduled verification of the sources works: status, last_success, last_failure
   * and consecutive_failures, as in a result.
   */
  verification: Record<string, unknown>;
}

/**
 * Whether the scheduled verification of the official sources works.
 */
export interface Verification {
  /**
   * How many verifications failed in a row, the latest included.
   */
  consecutive_failures: number;
  /**
   * When it last failed.
   */
  last_failure: string | null;
  /**
   * When it last worked.
   */
  last_success: string | null;
  /**
   * healthy: the last verification worked. failing: the last ones failed. unknown: none has
   * run.
   */
  status: "healthy" | "failing" | "unknown";
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
