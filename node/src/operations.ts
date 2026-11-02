// The operations of the TariffTrust API, as methods. Generated from openapi.json by scripts/generate.py: do not edit.

import type { Call, RequestOptions } from "./call.js";
import type {
  AgreementList,
  BatchRequest,
  BatchResult,
  CalculationResult,
  EntryInput,
  EntryResult,
  EstimateInput,
  FactList,
  HistoryRequest,
  HistoryResult,
  HtsDetail,
  HtsSearch,
  ListSavedEstimatesQuery,
  SaveRequest,
  Saved,
  SavedDetail,
  SavedList,
  SearchHtsQuery,
  Status,
} from "./types.js";

/** Each operation of the contract, under its operationId in camelCase. */
export abstract class Operations {
  protected abstract request<T>(call: Call): Promise<T>;

  /**
   * List the trade agreements.
   *
   * The agreements the engine applies, by the symbol of the HTS special column, with the
   * origins each can apply to. A symbol does not establish eligibility: send it as preference,
   * which declares the rules of origin met. Needs the read permission; not counted.
   */
  listAgreements(options?: RequestOptions): Promise<AgreementList> {
    return this.request<AgreementList>({
      method: "GET",
      path: "/v1/agreements",
      options,
    });
  }

  /**
   * Estimate one product.
   *
   * Every US duty and fee that applies to one product at a date, each with its official source.
   * Without a customs value, the duty rate. Not saved: an unsaved estimate cannot be replayed,
   * reported or notified in an incident; save it with POST /v1/saved-estimates. Needs the
   * calculate permission; counted in the quota unless it gives no figure of the duty: a
   * question asked without any duty amount or rate (status needs_information), a code the
   * tariff does not have or that names no product, a regime the service does not calculate. A
   * question that gives the duty of each answer (scenarios), their bounds or the subtotal
   * already known is counted.
   */
  estimate(body: EstimateInput, options?: RequestOptions): Promise<CalculationResult> {
    return this.request<CalculationResult>({
      method: "POST",
      path: "/v1/estimates",
      body,
      idempotent: true,
      options,
    });
  }

  /**
   * Estimate up to 200 products.
   *
   * Each item calculated on its own, as POST /v1/estimates would, in the order given. An
   * invalid item refuses the whole batch (422, error.fields naming items.<index>.<field>); an
   * item that cannot be calculated (a date no edition covers) has its own error in results, the
   * others are calculated. The batch's publication_id, if any, holds for every item. Counted as
   * one request, whatever its number of items, unless none of them gives a figure of the duty
   * (questions without any duty amount or rate, and errors, only). When the data is unavailable
   * for every item, the batch is a 503 to send again, neither counted nor kept for its
   * Idempotency-Key; when only for some, they have their error (data_unavailable) in results:
   * send those items again.
   */
  estimateBatch(body: BatchRequest, options?: RequestOptions): Promise<BatchResult> {
    return this.request<BatchResult>({
      method: "POST",
      path: "/v1/estimates/batch",
      body,
      idempotent: true,
      options,
    });
  }

  /**
   * Estimate a whole import declaration.
   *
   * Every line, then the MPF and the HMF once on the declaration: adding the estimates of the
   * lines of one declaration gives a wrong MPF. Not saved: save it with POST /v1/saved-
   * estimates (entry) to replay or report it. Counted as one request, whatever its number of
   * lines, unless it gives no figure of the duty (a question without any duty amount or rate).
   */
  estimateEntry(body: EntryInput, options?: RequestOptions): Promise<EntryResult> {
    return this.request<EntryResult>({
      method: "POST",
      path: "/v1/estimates/entry",
      body,
      idempotent: true,
      options,
    });
  }

  /**
   * Estimate one product at every change of the tariff.
   *
   * The product calculated on each first day of an edition, on each day a measure or a fee that
   * covers it begins or ends, and on each day an incident or a notice not yet read begins or
   * stops withholding its estimate, over the period asked, with the rules approved today.
   * Counted as one request, whatever its number of points, unless no point gives a figure of
   * the duty (a question without any duty amount or rate).
   */
  estimateHistory(body: HistoryRequest, options?: RequestOptions): Promise<HistoryResult> {
    return this.request<HistoryResult>({
      method: "POST",
      path: "/v1/estimates/history",
      body,
      idempotent: true,
      options,
    });
  }

  /**
   * List the questions an estimate may ask.
   *
   * The facts catalogue: each question a measure may depend on, by the name to answer it with
   * in facts, its type, its choices and its ordinary case. A result lists the ones it needs in
   * input_guidance, and those it assumed in assumptions. Needs the read permission; not
   * counted.
   */
  listFacts(options?: RequestOptions): Promise<FactList> {
    return this.request<FactList>({
      method: "GET",
      path: "/v1/facts",
      options,
    });
  }

  /**
   * Search the US tariff schedule.
   *
   * The lines of the edition in service whose code starts with q, or whose descriptions hold
   * every word of q, in code order; chapter (two digits) narrows them. A match is no
   * classification. Needs the read permission; not counted.
   */
  searchHts(query: SearchHtsQuery = {}, options?: RequestOptions): Promise<HtsSearch> {
    return this.request<HtsSearch>({
      method: "GET",
      path: "/v1/hts",
      query: query as Record<string, unknown>,
      options,
    });
  }

  /**
   * Read one line of the US tariff schedule.
   *
   * One line of the edition in service: its descriptions, its rate columns and its units. Needs
   * the read permission; not counted.
   */
  getHts(code: string, options?: RequestOptions): Promise<HtsDetail> {
    return this.request<HtsDetail>({
      method: "GET",
      path: `/v1/hts/${encodeURIComponent(code)}`,
      options,
    });
  }

  /**
   * List the saved estimates.
   *
   * The workspace's saved estimates, the latest first, saved from the API, the MCP or the
   * portal. Needs the read permission; not counted.
   */
  listSavedEstimates(query: ListSavedEstimatesQuery = {}, options?: RequestOptions): Promise<SavedList> {
    return this.request<SavedList>({
      method: "GET",
      path: "/v1/saved-estimates",
      query: query as Record<string, unknown>,
      options,
    });
  }

  /**
   * Calculate and save an estimate.
   *
   * Calculate one product (estimate) or a declaration (entry) as POST /v1/estimates or POST
   * /v1/estimates/entry would, and save it: only a saved estimate can be replayed, reported or
   * notified in an incident. Needs the calculate permission; counted as the estimate is.
   * Whichever is saved, an Idempotency-Key holds for one request of this route.
   */
  saveEstimate(body: SaveRequest, options?: RequestOptions): Promise<Saved> {
    return this.request<Saved>({
      method: "POST",
      path: "/v1/saved-estimates",
      body,
      idempotent: true,
      options,
    });
  }

  /**
   * Read a saved estimate.
   *
   * One saved estimate: its request, as the engine read it, its result as it was calculated,
   * never recalculated, and the incidents found since that concern it. Needs the read
   * permission; not counted.
   */
  getSavedEstimate(id: string, options?: RequestOptions): Promise<SavedDetail> {
    return this.request<SavedDetail>({
      method: "GET",
      path: `/v1/saved-estimates/${encodeURIComponent(id)}`,
      options,
    });
  }

  /**
   * Read the status and the coverage of the data.
   *
   * Freshness and verification of the data, the share of estimates withheld, the publications
   * and the engine in service, and what is covered: Chapter 99 positions and their status,
   * historical periods, base rates, agreements, fees, and what is out of scope. No key needed;
   * the pages /status/ and /coverage/ read the same sources.
   */
  getStatus(options?: RequestOptions): Promise<Status> {
    return this.request<Status>({
      method: "GET",
      path: "/v1/status",
      auth: false,
      options,
    });
  }
}
