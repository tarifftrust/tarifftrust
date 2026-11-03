"""The objects of the TariffTrust API. Generated from openapi.json by scripts/generate.py: do not edit."""


from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import date, datetime
from decimal import Decimal
from typing import Any, ClassVar, Literal, TypedDict

from ._model import Model


class _BatchItemRequired(TypedDict):
    hts: str
    """The HTS code of the goods: 4, 6, 8 or 10 digits, dots and spaces ignored. A rate needs
    the 10-digit statistical line or its 8-digit subheading.
    """
    origin: str
    """Country of origin: where the goods were produced, not where they ship from. ISO 3166-1
    alpha-2 (XK for Kosovo), or a code U.S. Customs files with (BU, GZ, KV, WE).
    """


class BatchItem(_BatchItemRequired, total=False):
    """One product of a batch: the batch's publication, if any, applies to every item."""
    as_of: str | date | datetime | None
    """When the goods are entered for consumption. A day, in New York time ("2026-04-05"); or,
    on a day when a measure takes effect at a stated hour, the instant of entry with its UTC
    offset ("2026-04-05T00:01:00-04:00"). Unset: today.
    """
    customs_value: int | float | Decimal | str | None
    """Customs value in US dollars: the transaction value declared, not a retail price. Unset:
    the duty rate is given, and an amount only where the duty does not depend on the value.
    """
    entry_type: Literal["formal", "informal"]
    """A formal entry pays the merchandise processing fee (MPF) on its value; an informal one,
    the fixed informal fee.
    """
    facts: Mapping[str, int | float | Decimal | str | bool]
    """Answers to the questions of the facts catalogue (GET /v1/facts), by name. A name outside
    the catalogue is reported in the result and never used.
    """
    freight: int | float | Decimal | str
    """International freight in US dollars: no duty on it, it adds to the landed cost."""
    include_fees: bool
    """Count the entry fees (MPF, HMF) of a declaration of this product alone; the landed cost
    includes them only then. The MPF is charged once on a declaration: for several products
    entered together, use POST /v1/estimates/entry.
    """
    insurance: int | float | Decimal | str
    """Insurance of the shipment in US dollars: no duty on it, it adds to the landed cost."""
    preference: str | None
    """A trade agreement's symbol from the HTS special column (S for USMCA, KR for KORUS…; GET
    /v1/agreements). Giving it declares that the goods meet its rules of origin and that you
    hold the proof.
    """
    quantities: Mapping[str, int | float | Decimal | str]
    """Quantities in the units a duty counts (kg, l, item, dozen, pair, proof_liter…),
    nonnegative. A result names the quantity it needs in required_fields ("quantities.kg").
    """
    transport_mode: Literal["air", "ocean", "land"] | None
    """How the goods arrive; by sea they also pay the harbor maintenance fee (HMF). Unset: land
    for goods of Canada or Mexico, ocean otherwise.
    """


class _EntryInputRequired(TypedDict):
    lines: Sequence[LineInput]
    """The lines of the declaration, each a product."""


class EntryInput(_EntryInputRequired, total=False):
    """A whole import declaration: every line, then the MPF and the HMF once on the
    declaration. POST /v1/estimates/entry.
    """
    as_of: str | date | datetime | None
    """When the goods are entered for consumption. A day, in New York time ("2026-04-05"); or,
    on a day when a measure takes effect at a stated hour, the instant of entry with its UTC
    offset ("2026-04-05T00:01:00-04:00"). Unset: today.
    """
    entry_type: Literal["formal", "informal"]
    """A formal entry pays the merchandise processing fee (MPF) on its value; an informal one,
    the fixed informal fee.
    """
    facts: Mapping[str, int | float | Decimal | str | bool]
    """Answers that hold for the whole declaration (GET /v1/facts, scope entry or shipment)."""
    freight: int | float | Decimal | str
    """International freight in US dollars: no duty on it, it adds to the landed cost."""
    include_fees: bool
    """Count the entry fees (MPF, HMF) of the declaration."""
    insurance: int | float | Decimal | str
    """Insurance of the shipment in US dollars: no duty on it, it adds to the landed cost."""
    publication_id: str | None
    """Calculate with this publication of the rules rather than the one in force on the date: a
    saved result's publication_id replays it.
    """
    reference: str
    """Your reference for the declaration."""
    transport_mode: Literal["air", "ocean", "land"] | None
    """How the goods arrive; by sea they also pay the harbor maintenance fee (HMF). Unset: land
    for goods of Canada or Mexico, ocean otherwise.
    """


class _EstimateInputRequired(TypedDict):
    hts: str
    """The HTS code of the goods: 4, 6, 8 or 10 digits, dots and spaces ignored. A rate needs
    the 10-digit statistical line or its 8-digit subheading.
    """
    origin: str
    """Country of origin: where the goods were produced, not where they ship from. ISO 3166-1
    alpha-2 (XK for Kosovo), or a code U.S. Customs files with (BU, GZ, KV, WE).
    """


class EstimateInput(_EstimateInputRequired, total=False):
    """One product at a date: POST /v1/estimates."""
    as_of: str | date | datetime | None
    """When the goods are entered for consumption. A day, in New York time ("2026-04-05"); or,
    on a day when a measure takes effect at a stated hour, the instant of entry with its UTC
    offset ("2026-04-05T00:01:00-04:00"). Unset: today.
    """
    customs_value: int | float | Decimal | str | None
    """Customs value in US dollars: the transaction value declared, not a retail price. Unset:
    the duty rate is given, and an amount only where the duty does not depend on the value.
    """
    entry_type: Literal["formal", "informal"]
    """A formal entry pays the merchandise processing fee (MPF) on its value; an informal one,
    the fixed informal fee.
    """
    facts: Mapping[str, int | float | Decimal | str | bool]
    """Answers to the questions of the facts catalogue (GET /v1/facts), by name. A name outside
    the catalogue is reported in the result and never used.
    """
    freight: int | float | Decimal | str
    """International freight in US dollars: no duty on it, it adds to the landed cost."""
    include_fees: bool
    """Count the entry fees (MPF, HMF) of a declaration of this product alone; the landed cost
    includes them only then. The MPF is charged once on a declaration: for several products
    entered together, use POST /v1/estimates/entry.
    """
    insurance: int | float | Decimal | str
    """Insurance of the shipment in US dollars: no duty on it, it adds to the landed cost."""
    preference: str | None
    """A trade agreement's symbol from the HTS special column (S for USMCA, KR for KORUS…; GET
    /v1/agreements). Giving it declares that the goods meet its rules of origin and that you
    hold the proof.
    """
    publication_id: str | None
    """Calculate with this publication of the rules rather than the one in force on the date: a
    saved result's publication_id replays it.
    """
    quantities: Mapping[str, int | float | Decimal | str]
    """Quantities in the units a duty counts (kg, l, item, dozen, pair, proof_liter…),
    nonnegative. A result names the quantity it needs in required_fields ("quantities.kg").
    """
    transport_mode: Literal["air", "ocean", "land"] | None
    """How the goods arrive; by sea they also pay the harbor maintenance fee (HMF). Unset: land
    for goods of Canada or Mexico, ocean otherwise.
    """


class _LineInputRequired(TypedDict):
    hts: str
    """The HTS code of the goods: 4, 6, 8 or 10 digits, dots and spaces ignored. A rate needs
    the 10-digit statistical line or its 8-digit subheading.
    """
    origin: str
    """Country of origin: where the goods were produced, not where they ship from. ISO 3166-1
    alpha-2 (XK for Kosovo), or a code U.S. Customs files with (BU, GZ, KV, WE).
    """


class LineInput(_LineInputRequired, total=False):
    """One line of a declaration."""
    customs_value: int | float | Decimal | str | None
    """Customs value in US dollars: the transaction value declared, not a retail price. Unset:
    the duty rate is given, and an amount only where the duty does not depend on the value.
    """
    facts: Mapping[str, int | float | Decimal | str | bool]
    """Answers to the questions of the facts catalogue (GET /v1/facts), by name. A name outside
    the catalogue is reported in the result and never used.
    """
    preference: str | None
    """A trade agreement's symbol from the HTS special column (S for USMCA, KR for KORUS…; GET
    /v1/agreements). Giving it declares that the goods meet its rules of origin and that you
    hold the proof.
    """
    quantities: Mapping[str, int | float | Decimal | str]
    """Quantities in the units a duty counts (kg, l, item, dozen, pair, proof_liter…),
    nonnegative. A result names the quantity it needs in required_fields ("quantities.kg").
    """
    reference: str
    """Your reference for the line."""


class Agreement(Model):
    """A trade agreement, by its symbol in the HTS special column."""

    _fields: ClassVar[frozenset[str]] = frozenset(['any_column1_origin', 'name', 'origins', 'symbol'])
    _required: ClassVar[frozenset[str]] = frozenset(['any_column1_origin', 'name', 'origins', 'symbol'])

    any_column1_origin: bool
    """A product agreement open to any column 1 origin."""

    name: str | None
    """The agreement's common name, where it has one."""

    origins: list[str]
    """The origins it can apply to; none for a product agreement."""

    symbol: str
    """As the HTS special column prints it; send it as preference."""


class AgreementList(Model):
    """The trade agreements the engine applies."""

    _fields: ClassVar[frozenset[str]] = frozenset(['agreements', 'condition', 'source'])
    _required: ClassVar[frozenset[str]] = frozenset(['agreements', 'condition', 'source'])
    _nested: ClassVar[dict[str, Any]] = {'agreements': ['Agreement']}

    agreements: list[Agreement]
    """Each agreement the engine applies."""

    condition: str
    """What a symbol does not establish."""

    source: str
    """Where the tariff that names them is published."""


class BatchFailure(Model):
    """An item of a batch that could not be calculated; the others are."""

    _fields: ClassVar[frozenset[str]] = frozenset(['error', 'index'])
    _required: ClassVar[frozenset[str]] = frozenset(['error', 'index'])
    _nested: ClassVar[dict[str, Any]] = {'error': 'Error'}

    error: Error
    """Why it has no result: invalid_input with its fields, or no data for its date yet
    (data_unavailable, edition_not_published): send it again later.
    """

    index: int
    """The item's position in items, from 0."""


class BatchResult(Model):
    """The products of a batch, each calculated on its own."""

    _fields: ClassVar[frozenset[str]] = frozenset(['freshness', 'publication_id', 'publication_ids', 'results'])
    _required: ClassVar[frozenset[str]] = frozenset(['freshness', 'publication_id', 'publication_ids', 'results'])
    _nested: ClassVar[dict[str, Any]] = {'freshness': {'*': 'Freshness'}, 'results': [('BatchSuccess', 'BatchFailure')]}

    freshness: dict[str, Freshness]
    """The freshness of each publication used, by its id."""

    publication_id: str | None
    """The publication every item was calculated with; null when they differ (their dates do)."""

    publication_ids: list[str]
    """Every publication used."""

    results: list[BatchSuccess | BatchFailure]
    """One per item, in the order sent: its result, or its error."""


class BatchSuccess(Model):
    """An item of a batch that was calculated."""

    _fields: ClassVar[frozenset[str]] = frozenset(['index', 'result'])
    _required: ClassVar[frozenset[str]] = frozenset(['index', 'result'])
    _nested: ClassVar[dict[str, Any]] = {'result': 'CalculationResult'}

    index: int
    """The item's position in items, from 0."""

    result: CalculationResult
    """Its result, as POST /v1/estimates gives it, without last_approved."""


class CalculationResult(Model):
    """One product: the line, with the fees of its one-line declaration."""

    _fields: ClassVar[frozenset[str]] = frozenset(['alerts', 'answers', 'as_of', 'as_of_instant', 'assumptions', 'base_rate', 'candidates', 'column_rates', 'components', 'currency', 'description', 'duty_rate', 'engine_version', 'estimate_scope', 'estimated_duty', 'estimated_landed_cost', 'examined_measures', 'fees', 'fees_status', 'footnotes', 'freshness', 'hts', 'input_guidance', 'knowledge_at', 'known_duty_subtotal', 'known_fee_subtotal', 'known_ieepa_subtotal', 'last_approved', 'match', 'origin', 'policies', 'provenance', 'publication_checksum', 'publication_id', 'publication_label', 'reference', 'replaced_base', 'required_fields', 'reserved_components', 'review_pending', 'scenarios', 'sources', 'statistical_units', 'status', 'total_fees', 'verification', 'warnings'])
    _required: ClassVar[frozenset[str]] = frozenset(['as_of', 'base_rate', 'components', 'currency', 'engine_version', 'estimate_scope', 'estimated_duty', 'estimated_landed_cost', 'fees', 'fees_status', 'hts', 'knowledge_at', 'known_duty_subtotal', 'match', 'origin', 'publication_checksum', 'publication_id', 'publication_label', 'required_fields', 'sources', 'status', 'total_fees', 'warnings'])
    _nested: ClassVar[dict[str, Any]] = {'candidates': ['Candidate'], 'components': ['Component'], 'duty_rate': 'DutyRate', 'examined_measures': ['ExaminedMeasure'], 'fees': ['Fee'], 'freshness': 'Freshness', 'input_guidance': ['InputGuidance'], 'last_approved': 'LastApproved', 'match': 'Match', 'reserved_components': ['Component'], 'review_pending': ['ReviewPending'], 'scenarios': 'Scenarios', 'sources': ['Source'], 'verification': 'Verification'}
    _defaults: ClassVar[dict[str, Any]] = {'alerts': [], 'answers': [], 'assumptions': [], 'examined_measures': [], 'policies': [], 'reserved_components': [], 'review_pending': []}

    alerts: list[str]
    """Measures whose relations do not settle (two caps on the same duties, contradictory
    relations): the duties concerned stay unresolved, and estimated_duty is null.
    """

    answers: list[dict[str, Any]]
    """The facts the request answered, each with the measures it decides (those whose decision
    another answer would change); none when, given the other answers, it decides nothing.
    """

    as_of: str
    """The legal day the duties are calculated for, in New York time."""

    as_of_instant: str | None
    """Instant of effect (New York time) when a transition on that day depends on the hour."""

    assumptions: list[dict[str, Any]]
    """The answers this estimate assumed because none was declared (the ordinary case): for
    each, the fact, the value assumed, its question, its type and choices, and under
    alternatives what each other answer would give. Send your own answer in facts to replace
    one.
    """

    base_rate: str | None
    """The base rate as the tariff prints it, in the column read: general, special (an
    agreement claimed and granted) or column 2.
    """

    candidates: list[Candidate] | None
    """With a shorter code: the 8- and 10-digit lines under it, up to 25."""

    column_rates: dict[str, str] | None
    """The line's three rate columns as printed: general, special and other (column 2)."""

    components: list[Component]
    """The duties counted, the base duty first, each with its amount and its source."""

    currency: Literal["USD"]
    """Always USD: every amount is in US dollars."""

    description: str | None
    """The line's descriptions, from the heading down."""

    duty_rate: DutyRate | None
    """The duty as a share of the customs value, for comparison."""

    engine_version: str
    """The version of the engine that calculated it."""

    estimate_scope: str
    """What the estimate covers, in words: implemented measures only, unknown never zero."""

    estimated_duty: str | None
    """Implemented measures only. Null means unknown, never zero: information is missing, a
    position is in review or an incident suspends it.
    """

    estimated_landed_cost: str | None
    """Customs value + estimated duty + freight + insurance, and the entry fees only when
    include_fees was asked. Null while the duty, an asked fee or the value is unknown.
    """

    examined_measures: list[ExaminedMeasure]
    """Decision, reason and source of every measure examined for this case."""

    fees: list[Fee]
    """The entry fees asked (include_fees), for a declaration of this product."""

    fees_status: Literal["not_requested", "not_covered", "estimated", "partial"]
    """not_requested: include_fees is false. estimated: every fee owed is known. partial: one
    is not (a value is missing, or the date or entry type has no fee schedule). not_covered:
    an entry regime outside the service, no fee calculated. include_fees is false by default
    for one product.
    """

    footnotes: list[Any] | None
    """The tariff's footnotes for the line, which may impose conditions."""

    freshness: Freshness | None
    """Whether the sources were verified recently enough."""

    hts: str
    """The HTS code calculated, in digits."""

    input_guidance: list[InputGuidance] | None
    """One question per missing input, to ask before calculating again."""

    knowledge_at: str | None
    """When the publication was prepared: the state of knowledge the result rests on."""

    known_duty_subtotal: str | None
    """Sum of the components whose validity is established; null when none is."""

    known_fee_subtotal: str | None
    """Sum of the fees established in fees; null when fees is empty (not asked, or no fee
    established for this date, entry type or regime).
    """

    known_ieepa_subtotal: str | None
    """In a history: the IEEPA duties established at that point; 0.00 when none applies, from
    2026-02-24; null otherwise.
    """

    last_approved: LastApproved | None
    """When positions in review or incidents withhold part of the result: the last result
    established without them, dated. Historical only: never part of a subtotal, total or
    exposure. Absent from batch items.
    """

    match: Match
    """How the code was found in the tariff."""

    origin: str
    """The country of origin, as sent."""

    policies: list[dict[str, Any]]
    """The workspace's standing answers applied, each marked when the request overrode it."""

    provenance: dict[str, Any] | None
    """What identifies this result for a replay: the engine result's checksum, the request as
    the engine read it, the legal end of its publication and the image of the engine.
    """

    publication_checksum: str | None
    """The checksum of that publication's files."""

    publication_id: str
    """The publication of the rules it was calculated with: send it as publication_id to
    calculate again with the same rules.
    """

    publication_label: str
    """The edition of the US tariff, in words."""

    reference: str | None
    """Your reference for the line, as sent."""

    replaced_base: dict[str, Any] | None
    """When a measure replaces the base duty: the base duty replaced, with the reason; in no
    total.
    """

    required_fields: list[str]
    """The inputs still missing, each asked in input_guidance."""

    reserved_components: list[Component]
    """Shown apart, subject to a position in review; in no total."""

    review_pending: list[ReviewPending]
    """What withholds part of the estimate: a position in review (position), a wrong-rate
    incident (incident), an official notice not yet read (notice), a measure in force whose
    rate is not announced yet (pending_rate).
    """

    scenarios: Scenarios | None
    """With unanswered yes/no or choice facts that have no ordinary case, every coherent
    combination of their answers (up to twelve) and exact bounds; beyond, a prudent range.
    Null otherwise.
    """

    sources: list[Source]
    """Every official document the result rests on."""

    statistical_units: list[str] | None
    """The statistical units the tariff prints for the line (No., kg)."""

    status: Literal["calculated", "partial", "needs_information", "unsupported", "not_found", "not_covered"]
    """What the answer is, to read before its amounts. calculated: every component is
    established. needs_information: what you can give is missing (a fact, a quantity, the
    value, a more precise code or the instant of effect), asked in input_guidance. partial:
    a component stays unknown that you cannot give (a position in review, an incident,
    incomplete coverage), listed in review_pending. unsupported: a rate, a formula or an
    entry regime the engine does not calculate. not_covered: a date or a chapter outside the
    data, or a code of chapters 98 and 99, which needs the product's own code. not_found: no
    such code in the tariff, nor any more precise one.
    """

    total_fees: str | None
    """The entry fees (MPF, HMF) of a declaration of this product alone, when include_fees was
    asked; null when they were not asked, or while one of them is not established.
    """

    verification: Verification | None
    """Whether the scheduled verification of the sources works; separate from freshness."""

    warnings: list[str]
    """Cautions in words, to show with the result: a preference declared, footnotes, fees not
    established, sources not verified recently.
    """


class Candidate(Model):
    """A line of the tariff under a code too short to calculate."""

    _fields: ClassVar[frozenset[str]] = frozenset(['description', 'hts'])
    _required: ClassVar[frozenset[str]] = frozenset(['description', 'hts'])

    description: str
    """Its description."""

    hts: str
    """A line under the code sent, of 8 or 10 digits."""


class Component(Model):
    """One duty counted in the result: the base duty, a Chapter 99 measure, or a cap's
    deduction.
    """

    _fields: ClassVar[frozenset[str]] = frozenset(['amount', 'expression', 'heading', 'id', 'label', 'program', 'required_fields', 'role', 'rule', 'rule_version', 'source', 'status', 'terms', 'uncertain'])
    _required: ClassVar[frozenset[str]] = frozenset(['amount', 'id', 'label', 'program', 'required_fields', 'source', 'status', 'terms'])
    _nested: ClassVar[dict[str, Any]] = {'source': 'Source', 'terms': ['RateTerm']}

    amount: str | None
    """The duty in dollars; null when unknown (an input is missing, or the rate is not
    calculated or not announced yet). Negative for a cap's deduction.
    """

    expression: str | None
    """The base rate as the tariff prints it; null for a measure, whose rate is in terms."""

    heading: str | None
    """The measure's Chapter 99 heading; null for the base duty."""

    id: str
    """base_rate for the base duty; otherwise the identifier of the measure."""

    label: str
    """The duty in words: Base duty, Column 2, or the measure's title."""

    program: str
    """base for the base duty; otherwise the measure's program, as 301, 232, 201 or 338."""

    required_fields: list[str]
    """The inputs its amount still needs: customs_value, quantities.<unit>, facts.<name>."""

    role: str | None
    """cap for a ceiling's deduction: what exceeds the ceiling, taken off the duties it limits.
    Absent otherwise.
    """

    rule: str | None
    """The identifier of the rule the measure comes from. Null for the base duty."""

    rule_version: str | None
    """The version of that rule."""

    source: Source
    """The official document of this rate."""

    status: Literal["calculated", "needs_information", "unsupported", "pending"]
    """calculated: the amount is established. needs_information: an input is missing, named in
    required_fields. unsupported: a rate the engine does not calculate. pending: in force at
    a rate the official text has not announced yet.
    """

    terms: list[RateTerm] | None
    """The rate as typed terms, added together; null when the printed rate cannot be read."""

    uncertain: bool | None
    """May still be removed by an unanswered question: shown, but not in known_duty_subtotal."""


class CoveredWindow(Model):
    """A period the service holds rules for, and the publication that covers it."""

    _fields: ClassVar[frozenset[str]] = frozenset(['from', 'publication_id', 'through'])
    _required: ClassVar[frozenset[str]] = frozenset(['from', 'publication_id', 'through'])

    from_: str
    """Its first day."""

    publication_id: str
    """The publication used over this window."""

    through: str
    """Its last day."""


class DutyRate(Model):
    """The duty as a share of the customs value, for comparison: implemented duties only,
    without the fees and AD/CVD.
    """

    _fields: ClassVar[frozenset[str]] = frozenset(['basis', 'estimated_ad_valorem_rate', 'status', 'total_ad_valorem_rate'])
    _required: ClassVar[frozenset[str]] = frozenset(['status'])

    basis: str | None
    """What the rate is, in words."""

    estimated_ad_valorem_rate: str | None
    """The duty as a decimal fraction of the customs value (0.415 for 41.5%)."""

    status: Literal["not_covered", "needs_information", "unsupported", "not_representable", "estimated", "complete"]
    """complete: the result is calculated and every duty is a share of the value. estimated:
    the share of the duties known, the result not settled. needs_information: an input other
    than the value is missing. not_representable: a duty is no share of the value (per unit,
    capped or undecided). unsupported: a rate the engine does not read. not_covered: no rate
    is read.
    """

    total_ad_valorem_rate: str | None
    """The same, given only when the status is complete."""


class EntryResult(Model):
    """A whole declaration: its lines, then its fees, once."""

    _fields: ClassVar[frozenset[str]] = frozenset(['as_of', 'as_of_instant', 'currency', 'engine_version', 'entry_type', 'estimate_scope', 'estimated_duty', 'estimated_landed_cost', 'fees', 'fees_status', 'freshness', 'input_guidance', 'kind', 'knowledge_at', 'known_duty_subtotal', 'last_approved', 'lines', 'policies', 'provenance', 'publication_checksum', 'publication_id', 'publication_label', 'reference', 'required_fields', 'scenarios', 'status', 'total_fees', 'transport_mode', 'verification', 'warnings'])
    _required: ClassVar[frozenset[str]] = frozenset(['as_of', 'estimated_duty', 'estimated_landed_cost', 'fees', 'fees_status', 'kind', 'known_duty_subtotal', 'lines', 'publication_id', 'required_fields', 'scenarios', 'status', 'total_fees', 'warnings'])
    _nested: ClassVar[dict[str, Any]] = {'fees': ['Fee'], 'freshness': 'Freshness', 'input_guidance': ['InputGuidance'], 'last_approved': 'LastApproved', 'lines': ['LineResult'], 'scenarios': 'Scenarios', 'verification': 'Verification'}
    _defaults: ClassVar[dict[str, Any]] = {'policies': []}

    as_of: str
    """The legal day of the declaration, in New York time."""

    as_of_instant: str | None
    """Instant of effect (New York time) when a transition on that day depends on the hour."""

    currency: Literal["USD"] | None
    """Always USD: every amount is in US dollars."""

    engine_version: str | None
    """The version of the engine that calculated it."""

    entry_type: str | None
    """formal or informal, as sent."""

    estimate_scope: str | None
    """What the estimate covers, in words: implemented measures only, unknown never zero."""

    estimated_duty: str | None
    """The duty of the declaration; null unless every line's is known. Unknown is never zero."""

    estimated_landed_cost: str | None
    """Customs values + estimated duty + freight + insurance, and the entry fees when
    include_fees (true by default for a declaration). Null while the duty, an asked fee or a
    value is unknown.
    """

    fees: list[Fee]
    """MPF and HMF, once for the declaration."""

    fees_status: Literal["not_requested", "not_covered", "estimated", "partial"]
    """not_requested: include_fees is false. estimated: every fee owed is known. partial: one
    is not (a value is missing, or the date or entry type has no fee schedule). not_covered:
    an entry regime outside the service, no fee calculated. include_fees is true by default
    for a declaration.
    """

    freshness: Freshness | None
    """Whether the sources were verified recently enough."""

    input_guidance: list[InputGuidance] | None
    """Empty: each line asks its own questions, in lines."""

    kind: Literal["entry"]
    """Always entry."""

    knowledge_at: str | None
    """When the publication was prepared: the state of knowledge the result rests on."""

    known_duty_subtotal: str | None
    """Sum of the lines' established subtotals; null when none is."""

    last_approved: LastApproved | None
    """When positions in review or incidents withhold part of the result: the last result
    established without them, dated. Historical only: never part of a subtotal, total or
    exposure. Absent from batch items.
    """

    lines: list[LineResult]
    """Each line's result, in the order sent."""

    policies: list[dict[str, Any]]
    """The workspace's standing answers applied, each marked when the request overrode it."""

    provenance: dict[str, Any] | None
    """What identifies this result for a replay: the engine result's checksum, the request as
    the engine read it, the legal end of its publication and the image of the engine.
    """

    publication_checksum: str | None
    """The checksum of that publication's files."""

    publication_id: str
    """The publication of the rules it was calculated with: send it as publication_id to
    calculate again with the same rules.
    """

    publication_label: str | None
    """The edition of the US tariff, in words."""

    reference: str | None
    """Your reference for the declaration, as sent."""

    required_fields: list[str]
    """Empty: each line names its own, in lines."""

    scenarios: Scenarios | None
    """With unanswered yes/no or choice facts that have no ordinary case, every coherent
    combination of their answers (up to twelve) and exact bounds; beyond, a prudent range.
    Null otherwise.
    """

    status: Literal["calculated", "partial", "needs_information", "unsupported", "not_found", "not_covered"]
    """The status of the declaration: that of its least settled line."""

    total_fees: str | None
    """The entry fees (MPF, HMF) of the declaration, counted once; null when include_fees is
    false, or while one of them is not established.
    """

    transport_mode: str | None
    """The transport mode, as sent or inferred."""

    verification: Verification | None
    """Whether the scheduled verification of the sources works; separate from freshness."""

    warnings: list[str]
    """Cautions on the declaration: its fees, the freshness and verification of the sources;
    each line has its own.
    """


class Error(Model):
    """What was refused, and why."""

    _fields: ClassVar[frozenset[str]] = frozenset(['code', 'fields', 'message'])
    _required: ClassVar[frozenset[str]] = frozenset(['code'])

    code: str
    """What went wrong, for a program: invalid_input, quota_exceeded, rate_limited,
    data_unavailable…
    """

    fields: list[str] | None
    """With invalid_input: each field refused, by its path (items.3.hts)."""

    message: str | None
    """The same in words, for a person."""


class ErrorResponse(Model):
    """Every error of the API."""

    _fields: ClassVar[frozenset[str]] = frozenset(['error', 'request_id'])
    _required: ClassVar[frozenset[str]] = frozenset(['error'])
    _nested: ClassVar[dict[str, Any]] = {'error': 'Error'}

    error: Error
    """The error."""

    request_id: str | None
    """The request's identifier, also in X-Request-ID: quote it to support."""


class ExaminedMeasure(Model):
    """The decision on every Chapter 99 measure examined for this case."""

    _fields: ClassVar[frozenset[str]] = frozenset(['decision', 'facts', 'heading', 'label', 'measure', 'program', 'reason', 'rule', 'rule_version', 'source'])
    _required: ClassVar[frozenset[str]] = frozenset(['decision', 'heading', 'label', 'measure', 'program', 'reason', 'rule', 'rule_version', 'source'])
    _nested: ClassVar[dict[str, Any]] = {'source': 'Source'}
    _defaults: ClassVar[dict[str, Any]] = {'facts': []}

    decision: Literal["applied", "excluded", "undetermined"]
    """applied: its conditions hold. excluded: one fails, or another measure removes it.
    undetermined: an unanswered question decides.
    """

    facts: list[str]
    """The facts its conditions read: the questions this measure decides."""

    heading: str
    """Its Chapter 99 heading."""

    label: str
    """Its title."""

    measure: str
    """The identifier of the measure."""

    program: str
    """Its program, as 301, 232, 201 or 338."""

    reason: str
    """Why, in words: the condition that decided, or what removed it."""

    rule: str
    """The identifier of the rule the measure comes from."""

    rule_version: str | None
    """The version of that rule."""

    source: Source
    """The official document of the measure."""


class FactChoice(Model):
    """One answer a choice question takes."""

    _fields: ClassVar[frozenset[str]] = frozenset(['label', 'value'])
    _required: ClassVar[frozenset[str]] = frozenset(['value'])

    label: str | None
    """The choice in words."""

    value: Any
    """The value to send in facts."""


class FactDefinition(Model):
    """A question an estimate may ask about the goods or the declaration."""

    _fields: ClassVar[frozenset[str]] = frozenset(['choices', 'default', 'help', 'name', 'question', 'scope', 'type', 'unit'])
    _required: ClassVar[frozenset[str]] = frozenset(['help', 'name', 'question', 'scope', 'type'])
    _nested: ClassVar[dict[str, Any]] = {'choices': ['FactChoice']}
    _defaults: ClassVar[dict[str, Any]] = {'choices': [], 'unit': ''}

    choices: list[FactChoice]
    """For a choice: the values to choose from."""

    default: Any
    """The ordinary case, assumed when unanswered and said in assumptions."""

    help: str
    """What it means, and how to answer it."""

    name: str
    """The key to answer it with, in facts."""

    question: str
    """The question to ask."""

    scope: str
    """product: a line's own; entry or shipment: the whole declaration's, one value for all its
    lines.
    """

    type: str
    """How it is answered: boolean (true or false), choice (one of choices), money (US
    dollars), number, country (ISO code) or heading (a Chapter 99 heading).
    """

    unit: str
    """The unit of a number, if any."""


class FactList(Model):
    """The facts catalogue: every question an estimate may ask."""

    _fields: ClassVar[frozenset[str]] = frozenset(['facts'])
    _required: ClassVar[frozenset[str]] = frozenset(['facts'])
    _nested: ClassVar[dict[str, Any]] = {'facts': ['FactDefinition']}

    facts: list[FactDefinition]
    """Every question of the catalogue."""


class Fee(Model):
    """An entry fee, once for the declaration."""

    _fields: ClassVar[frozenset[str]] = frozenset(['amount', 'assumption', 'basis', 'label', 'source'])
    _required: ClassVar[frozenset[str]] = frozenset(['amount', 'label', 'source'])
    _nested: ClassVar[dict[str, Any]] = {'source': 'Source'}

    amount: str | None
    """The fee in dollars; null when unknown."""

    assumption: str | None
    """The exemption it rests on, if any: declared, or that of goods originating under the
    agreement claimed.
    """

    basis: str | None
    """The value it is calculated on: the customs values of the lines subject to it; null when
    one is missing.
    """

    label: str
    """MPF (merchandise processing fee) or HMF (harbor maintenance fee)."""

    source: Source
    """The official fee schedule."""


class Freshness(Model):
    """How recently the official sources were verified."""

    _fields: ClassVar[frozenset[str]] = frozenset(['age_hours', 'basis', 'checked_at', 'stale'])
    _required: ClassVar[frozenset[str]] = frozenset(['age_hours', 'basis', 'checked_at', 'stale'])

    age_hours: float | None
    """Hours since then."""

    basis: str
    """The verification schedule and its target, or why a past edition has none."""

    checked_at: str | None
    """When the official sources were last verified successfully (before any verification, when
    the edition was observed); null for a past edition.
    """

    stale: bool
    """True past the freshness target: the sources may have changed since."""


class HistoryResult(Model):
    """One product at every change of the tariff over a period."""

    _fields: ClassVar[frozenset[str]] = frozenset(['basis', 'covered_windows', 'points'])
    _required: ClassVar[frozenset[str]] = frozenset(['basis', 'covered_windows', 'points'])
    _nested: ClassVar[dict[str, Any]] = {'covered_windows': ['CoveredWindow'], 'points': ['CalculationResult']}

    basis: str
    """How the points are calculated, in words."""

    covered_windows: list[CoveredWindow]
    """The periods the service holds rules for within the period asked: no point lies outside."""

    points: list[CalculationResult]
    """One result per change of the tariff, in date order, each on its as_of."""


class HtsDetail(Model):
    """One line of the tariff, with the descriptions above it and its footnotes."""

    _fields: ClassVar[frozenset[str]] = frozenset(['code', 'context', 'description', 'display_code', 'edition', 'footnotes', 'general', 'hierarchy', 'other', 'parent', 'publication_id', 'rate_from', 'special', 'units'])
    _required: ClassVar[frozenset[str]] = frozenset(['code', 'context', 'description', 'display_code', 'edition', 'general', 'hierarchy', 'other', 'parent', 'publication_id', 'rate_from', 'special', 'units'])
    _defaults: ClassVar[dict[str, Any]] = {'footnotes': []}

    code: str
    """10 digits for a statistical line, 8 for a subheading, 4 or 6 above."""

    context: str
    """The descriptions from the heading down to the line's own, joined by ›."""

    description: str
    """The line's own description."""

    display_code: str
    """The code as the tariff prints it (6109.10.00.12)."""

    edition: str
    """The edition of the US tariff, in words."""

    footnotes: list[Any]
    """The tariff's footnotes for the line."""

    general: str
    """Column 1 general rate, as printed."""

    hierarchy: list[str]
    """The descriptions above the line, from the heading down."""

    other: str
    """Column 2 rate."""

    parent: str
    """The code of the line above it."""

    publication_id: str
    """The publication in service."""

    rate_from: str | None
    """The 8-digit line whose rates a statistical line without its own takes, as the engine
    reads them; null when the rates are the line's own.
    """

    special: str
    """Column 1 special rates and the agreements that give them."""

    units: list[str]
    """The statistical units the tariff prints (No., kg)."""


class HtsLine(Model):
    """A line of the US tariff schedule, as its edition prints it."""

    _fields: ClassVar[frozenset[str]] = frozenset(['code', 'context', 'description', 'display_code', 'general', 'other', 'parent', 'special', 'units'])
    _required: ClassVar[frozenset[str]] = frozenset(['code', 'context', 'description', 'display_code', 'general', 'other', 'parent', 'special', 'units'])

    code: str
    """10 digits for a statistical line, 8 for a subheading, 4 or 6 above."""

    context: str
    """The descriptions from the heading down to the line's own, joined by ›."""

    description: str
    """The line's own description."""

    display_code: str
    """The code as the tariff prints it (6109.10.00.12)."""

    general: str
    """Column 1 general rate, as printed."""

    other: str
    """Column 2 rate."""

    parent: str
    """The code of the line above it."""

    special: str
    """Column 1 special rates and the agreements that give them."""

    units: list[str]
    """The statistical units the tariff prints (No., kg)."""


class HtsSearch(Model):
    """A page of the lines a search of the tariff finds."""

    _fields: ClassVar[frozenset[str]] = frozenset(['count', 'edition', 'limit', 'offset', 'publication_id', 'results'])
    _required: ClassVar[frozenset[str]] = frozenset(['count', 'edition', 'limit', 'offset', 'publication_id', 'results'])
    _nested: ClassVar[dict[str, Any]] = {'results': ['HtsLine']}

    count: int
    """How many lines match."""

    edition: str
    """The edition of the US tariff, in words."""

    limit: int
    """How many lines a page holds, as asked."""

    offset: int
    """How many lines were skipped, as asked."""

    publication_id: str
    """The publication in service."""

    results: list[HtsLine]
    """The lines of this page, in code order."""


class InputGuidance(Model):
    """One question for a missing input, to ask before calculating again."""

    _fields: ClassVar[frozenset[str]] = frozenset(['choices', 'description', 'field', 'kind', 'label', 'legal_basis', 'question', 'scope', 'type', 'unit'])
    _required: ClassVar[frozenset[str]] = frozenset(['description', 'field', 'label', 'type'])

    choices: list[Any] | None
    """The values to choose from, for a choice."""

    description: str
    """Why it is asked, or how to answer it."""

    field: str
    """Where to send the answer, as required_fields names it: facts.<name>, quantities.<unit>,
    customs_value, preference, hts or as_of.
    """

    kind: str | None
    """observable or choice (a fact of the goods), declared_conclusion (a conclusion you
    declare, as whether a Chapter 99 heading applies) or input (a plain input).
    """

    label: str
    """The question in a few words."""

    legal_basis: str | None
    """The text the question comes from."""

    question: str | None
    """The question to ask."""

    scope: str | None
    """product: the line's own; entry or shipment: the whole declaration's."""

    type: str
    """How it is answered: boolean, choice, money, number, country, heading, text or datetime."""

    unit: str | None
    """The unit of a number, if any."""


class LastApproved(Model):
    """The last result established without the items now withheld: historical, in no total."""

    _fields: ClassVar[frozenset[str]] = frozenset(['approved_from', 'approved_to', 'as_of', 'edition', 'estimated_duty', 'estimated_landed_cost', 'known_duty_subtotal', 'publication_id', 'status'])
    _required: ClassVar[frozenset[str]] = frozenset(['as_of', 'edition', 'estimated_duty', 'known_duty_subtotal', 'publication_id', 'status'])

    approved_from: str | None
    """When that publication was approved."""

    approved_to: str | None
    """Until when it was approved; null while it still is."""

    as_of: str
    """Legal date of this result; the edition's last day for an older edition."""

    edition: str
    """The edition of the US tariff, in words."""

    estimated_duty: str | None
    """The duty of that result."""

    estimated_landed_cost: str | None
    """The landed cost of that result."""

    known_duty_subtotal: str | None
    """The established subtotal of that result."""

    publication_id: str
    """The publication it was calculated with."""

    status: str
    """The status of that result."""


class LineResult(Model):
    """One line of a declaration: its duties. The fees and the landed cost are those of the
    declaration, calculated once for all its lines.
    """

    _fields: ClassVar[frozenset[str]] = frozenset(['alerts', 'answers', 'as_of', 'as_of_instant', 'assumptions', 'base_rate', 'candidates', 'column_rates', 'components', 'currency', 'description', 'duty_rate', 'engine_version', 'estimate_scope', 'estimated_duty', 'examined_measures', 'footnotes', 'hts', 'input_guidance', 'knowledge_at', 'known_duty_subtotal', 'match', 'origin', 'publication_checksum', 'publication_id', 'publication_label', 'reference', 'replaced_base', 'required_fields', 'reserved_components', 'review_pending', 'sources', 'statistical_units', 'status', 'warnings'])
    _required: ClassVar[frozenset[str]] = frozenset(['as_of', 'base_rate', 'components', 'currency', 'engine_version', 'estimate_scope', 'estimated_duty', 'hts', 'knowledge_at', 'known_duty_subtotal', 'match', 'origin', 'publication_checksum', 'publication_id', 'publication_label', 'required_fields', 'sources', 'status', 'warnings'])
    _nested: ClassVar[dict[str, Any]] = {'candidates': ['Candidate'], 'components': ['Component'], 'duty_rate': 'DutyRate', 'examined_measures': ['ExaminedMeasure'], 'input_guidance': ['InputGuidance'], 'match': 'Match', 'reserved_components': ['Component'], 'review_pending': ['ReviewPending'], 'sources': ['Source']}
    _defaults: ClassVar[dict[str, Any]] = {'alerts': [], 'answers': [], 'assumptions': [], 'examined_measures': [], 'reserved_components': [], 'review_pending': []}

    alerts: list[str]
    """Measures whose relations do not settle (two caps on the same duties, contradictory
    relations): the duties concerned stay unresolved, and estimated_duty is null.
    """

    answers: list[dict[str, Any]]
    """The facts the request answered, each with the measures it decides (those whose decision
    another answer would change); none when, given the other answers, it decides nothing.
    """

    as_of: str
    """The legal day the duties are calculated for, in New York time."""

    as_of_instant: str | None
    """Instant of effect (New York time) when a transition on that day depends on the hour."""

    assumptions: list[dict[str, Any]]
    """The answers this estimate assumed because none was declared (the ordinary case): for
    each, the fact, the value assumed, its question, its type and choices, and under
    alternatives what each other answer would give. Send your own answer in facts to replace
    one.
    """

    base_rate: str | None
    """The base rate as the tariff prints it, in the column read: general, special (an
    agreement claimed and granted) or column 2.
    """

    candidates: list[Candidate] | None
    """With a shorter code: the 8- and 10-digit lines under it, up to 25."""

    column_rates: dict[str, str] | None
    """The line's three rate columns as printed: general, special and other (column 2)."""

    components: list[Component]
    """The duties counted, the base duty first, each with its amount and its source."""

    currency: Literal["USD"]
    """Always USD: every amount is in US dollars."""

    description: str | None
    """The line's descriptions, from the heading down."""

    duty_rate: DutyRate | None
    """The duty as a share of the customs value, for comparison."""

    engine_version: str
    """The version of the engine that calculated it."""

    estimate_scope: str
    """What the estimate covers, in words: implemented measures only, unknown never zero."""

    estimated_duty: str | None
    """Implemented measures only. Null means unknown, never zero: information is missing, a
    position is in review or an incident suspends it.
    """

    examined_measures: list[ExaminedMeasure]
    """Decision, reason and source of every measure examined for this case."""

    footnotes: list[Any] | None
    """The tariff's footnotes for the line, which may impose conditions."""

    hts: str
    """The HTS code calculated, in digits."""

    input_guidance: list[InputGuidance] | None
    """One question per missing input, to ask before calculating again."""

    knowledge_at: str | None
    """When the publication was prepared: the state of knowledge the result rests on."""

    known_duty_subtotal: str | None
    """Sum of the components whose validity is established; null when none is."""

    match: Match
    """How the code was found in the tariff."""

    origin: str
    """The country of origin, as sent."""

    publication_checksum: str | None
    """The checksum of that publication's files."""

    publication_id: str
    """The publication of the rules it was calculated with: send it as publication_id to
    calculate again with the same rules.
    """

    publication_label: str
    """The edition of the US tariff, in words."""

    reference: str | None
    """Your reference for the line, as sent."""

    replaced_base: dict[str, Any] | None
    """When a measure replaces the base duty: the base duty replaced, with the reason; in no
    total.
    """

    required_fields: list[str]
    """The inputs still missing, each asked in input_guidance."""

    reserved_components: list[Component]
    """Shown apart, subject to a position in review; in no total."""

    review_pending: list[ReviewPending]
    """What withholds part of the estimate: a position in review (position), a wrong-rate
    incident (incident), an official notice not yet read (notice), a measure in force whose
    rate is not announced yet (pending_rate).
    """

    sources: list[Source]
    """Every official document the result rests on."""

    statistical_units: list[str] | None
    """The statistical units the tariff prints for the line (No., kg)."""

    status: Literal["calculated", "partial", "needs_information", "unsupported", "not_found", "not_covered"]
    """What the answer is, to read before its amounts. calculated: every component is
    established. needs_information: what you can give is missing (a fact, a quantity, the
    value, a more precise code or the instant of effect), asked in input_guidance. partial:
    a component stays unknown that you cannot give (a position in review, an incident,
    incomplete coverage), listed in review_pending. unsupported: a rate, a formula or an
    entry regime the engine does not calculate. not_covered: a date or a chapter outside the
    data, or a code of chapters 98 and 99, which needs the product's own code. not_found: no
    such code in the tariff, nor any more precise one.
    """

    warnings: list[str]
    """Cautions in words, to show with the result: a preference declared, footnotes, fees not
    established, sources not verified recently.
    """


class Match(Model):
    """How the code sent was found in the tariff."""

    _fields: ClassVar[frozenset[str]] = frozenset(['level', 'matched_hts', 'rate_basis', 'rate_hts', 'type'])
    _required: ClassVar[frozenset[str]] = frozenset(['level', 'rate_basis', 'type'])

    level: int
    """The number of digits of the code sent."""

    matched_hts: str | None
    """The line found."""

    rate_basis: Literal["direct", "parent"] | None
    """direct: the line's own rates. parent: a 10-digit line without rates of its own takes
    those of its 8-digit line.
    """

    rate_hts: str | None
    """The line whose rates are read."""

    type: Literal["none", "exact", "prefix_candidates"]
    """exact: a line of the tariff. prefix_candidates: a shorter code, the lines under it in
    candidates. none: not found, or not calculated (a date or chapter not covered).
    """


class RateTerm(Model):
    """One term of a rate; the terms of a rate are added together."""

    _fields: ClassVar[frozenset[str]] = frozenset(['amount', 'basis', 'field', 'kind', 'rate', 'unit'])
    _required: ClassVar[frozenset[str]] = frozenset(['kind'])

    amount: str | None
    """Dollars per unit, for a specific term."""

    basis: str | None
    """For a top_up, the duty it completes: applicable (the line's base duty) or mfn (the
    column 1 general duty).
    """

    field: str | None
    """The fact that gives the value the term applies to: the part's value (content), or the
    value a top_up covers.
    """

    kind: Literal["ad_valorem", "content", "named", "pending", "specific", "sugar", "top_up"]
    """The form of the term. ad_valorem: a share of the value. specific: an amount per unit.
    content: a share of the value of a part (a watch's movement). top_up: what brings the
    duty up to a share of the value. sugar: the polarization formula. named: a calculator of
    the engine. pending: announced without its rate.
    """

    rate: str | None
    """A decimal fraction (0.165 for 16.5%): of the value (ad_valorem), of the part's value
    (content), the share a top_up brings the duty to, or the sugar formula's rate per
    kilogram.
    """

    unit: str | None
    """The unit a specific term counts, as in quantities (kg, l, item…)."""


class ReviewPending(Model):
    """What withholds part of an estimate."""

    _fields: ClassVar[frozenset[str]] = frozenset(['detected_at', 'effect', 'kind', 'position', 'reason', 'reference'])
    _required: ClassVar[frozenset[str]] = frozenset(['effect', 'kind', 'reason'])

    detected_at: str | None
    """When it was detected."""

    effect: str
    """What it may do to the estimate: additional (a duty on top of the others), may_modify
    (change the duties it names, which are withheld), none, or unknown (change any duty: all
    are withheld).
    """

    kind: Literal["position", "incident", "notice", "pending_rate"]
    """position: a Chapter 99 position in review. incident: an open wrong-rate incident.
    notice: an official notice not yet read. pending_rate: a measure in force whose rate is
    not announced yet.
    """

    position: str | None
    """The Chapter 99 heading concerned, if any."""

    reason: str
    """Why the estimate is withheld, in words."""

    reference: str | None
    """The incident's or the notice's reference."""


class Saved(Model):
    """An estimate just calculated and saved."""

    _fields: ClassVar[frozenset[str]] = frozenset(['entry_id', 'id', 'kind', 'result'])
    _required: ClassVar[frozenset[str]] = frozenset(['id', 'kind', 'result'])
    _nested: ClassVar[dict[str, Any]] = {'result': ('CalculationResult', 'EntryResult')}

    entry_id: str | None
    """For a declaration: the declaration it is saved as in the portal."""

    id: str
    """The saved estimate's identifier."""

    kind: Literal["single", "entry"]
    """single: one product. entry: a declaration."""

    result: CalculationResult | EntryResult
    """Its result, as POST /v1/estimates or POST /v1/estimates/entry gives it."""


class SavedDetail(Model):
    """A saved estimate with its request and its result, as they were."""

    _fields: ClassVar[frozenset[str]] = frozenset(['author', 'created_at', 'engine_version', 'estimated_duty', 'id', 'image_digest', 'incidents', 'inputs', 'kind', 'label', 'publication_id', 'result', 'source', 'status'])
    _required: ClassVar[frozenset[str]] = frozenset(['author', 'created_at', 'engine_version', 'estimated_duty', 'id', 'image_digest', 'incidents', 'inputs', 'kind', 'label', 'publication_id', 'result', 'source', 'status'])
    _nested: ClassVar[dict[str, Any]] = {'incidents': ['SavedIncident']}

    author: str
    """Who saved it: the API key, by its name, or the person."""

    created_at: str
    """When it was saved."""

    engine_version: str
    """The version of the engine that calculated it."""

    estimated_duty: str | None
    """The duty of its result, as it was calculated."""

    id: str
    """Its identifier: read it with GET /v1/saved-estimates/{id}."""

    image_digest: str | None
    """The image of the engine that replays it exactly."""

    incidents: list[SavedIncident]
    """The incidents found since it was saved that concern it, the oldest first; empty when
    there are none.
    """

    inputs: dict[str, Any]
    """The request, in the fields of the API: an EstimateInput (single) or an EntryInput
    (entry).
    """

    kind: Literal["single", "entry"]
    """single: one product. entry: a declaration."""

    label: str
    """Its name, as given when saved."""

    publication_id: str | None
    """The publication it was calculated with."""

    result: dict[str, Any]
    """The result as its engine_version calculated it, never recalculated: a CalculationResult
    (single) or an EntryResult (entry) of that version.
    """

    source: str
    """Where it was saved: api, mcp, portal, import (a declaration imported in the portal) or
    report (the case of an error report).
    """

    status: str | None
    """The status of its result, as it was calculated: incidents says what was found since."""


class SavedIncident(Model):
    """An incident found since an estimate was saved, that concerns it."""

    _fields: ClassVar[frozenset[str]] = frozenset(['corrected_duty', 'corrected_fees', 'notice', 'outcome', 'reference'])
    _required: ClassVar[frozenset[str]] = frozenset(['corrected_duty', 'corrected_fees', 'notice', 'outcome', 'reference'])

    corrected_duty: str | None
    """The duty calculated again once verified; null while it is being verified."""

    corrected_fees: str | None
    """The entry fees calculated again once verified; null while it is being verified, or when
    they were not asked.
    """

    notice: str
    """What is being verified or was corrected, in words."""

    outcome: Literal["pending", "wrong", "unaffected"]
    """pending: being verified. wrong: confirmed wrong, the corrected figures say by how much.
    unaffected: verified, the figures saved stand.
    """

    reference: str
    """The incident, as the emails and the status page name it."""


class SavedList(Model):
    """A page of the workspace's saved estimates."""

    _fields: ClassVar[frozenset[str]] = frozenset(['count', 'limit', 'offset', 'results'])
    _required: ClassVar[frozenset[str]] = frozenset(['count', 'limit', 'offset', 'results'])
    _nested: ClassVar[dict[str, Any]] = {'results': ['SavedSummary']}

    count: int
    """How many saved estimates the workspace has."""

    limit: int
    """How many a page holds, as asked."""

    offset: int
    """How many were skipped, as asked."""

    results: list[SavedSummary]
    """This page, the latest first."""


class SavedSummary(Model):
    """A saved estimate, as the list gives it."""

    _fields: ClassVar[frozenset[str]] = frozenset(['author', 'created_at', 'engine_version', 'estimated_duty', 'id', 'image_digest', 'incidents', 'kind', 'label', 'publication_id', 'source', 'status'])
    _required: ClassVar[frozenset[str]] = frozenset(['author', 'created_at', 'engine_version', 'estimated_duty', 'id', 'image_digest', 'incidents', 'kind', 'label', 'publication_id', 'source', 'status'])
    _nested: ClassVar[dict[str, Any]] = {'incidents': ['SavedIncident']}

    author: str
    """Who saved it: the API key, by its name, or the person."""

    created_at: str
    """When it was saved."""

    engine_version: str
    """The version of the engine that calculated it."""

    estimated_duty: str | None
    """The duty of its result, as it was calculated."""

    id: str
    """Its identifier: read it with GET /v1/saved-estimates/{id}."""

    image_digest: str | None
    """The image of the engine that replays it exactly."""

    incidents: list[SavedIncident]
    """The incidents found since it was saved that concern it, the oldest first; empty when
    there are none.
    """

    kind: Literal["single", "entry"]
    """single: one product. entry: a declaration."""

    label: str
    """Its name, as given when saved."""

    publication_id: str | None
    """The publication it was calculated with."""

    source: str
    """Where it was saved: api, mcp, portal, import (a declaration imported in the portal) or
    report (the case of an error report).
    """

    status: str | None
    """The status of its result, as it was calculated: incidents says what was found since."""


class Scenario(Model):
    """One combination of answers to the questions left open, and what it gives."""

    _fields: ClassVar[frozenset[str]] = frozenset(['answers', 'estimated_duty', 'estimated_total', 'total_fees'])
    _required: ClassVar[frozenset[str]] = frozenset(['answers', 'estimated_duty', 'estimated_total', 'total_fees'])

    answers: list[dict[str, Any]]
    """One answer to each question: its fact, its line (from 0; null for a question of the
    whole declaration) and its value.
    """

    estimated_duty: str | None
    """The duty with these answers."""

    estimated_total: str | None
    """Duty and fees with these answers; null when one is unknown."""

    total_fees: str | None
    """The fees with these answers; null when not asked or unknown."""


class Scenarios(Model):
    """What the estimate would be under each answer to the questions that have no ordinary
    case.
    """

    _fields: ClassVar[frozenset[str]] = frozenset(['bounds', 'facts', 'kind', 'scenarios'])
    _required: ClassVar[frozenset[str]] = frozenset(['bounds', 'facts', 'kind', 'scenarios'])
    _nested: ClassVar[dict[str, Any]] = {'scenarios': ['Scenario']}

    bounds: dict[str, str] | None
    """minimum and maximum of estimated_total, with their label; null when a combination has no
    total.
    """

    facts: list[str]
    """The questions the scenarios answer."""

    kind: Literal["exact", "prudent"]
    """exact: every combination calculated. prudent: more than twelve, bounds only."""

    scenarios: list[Scenario]
    """Each combination; empty for a prudent range."""


class Source(Model):
    """An official document a rate, a measure or a fee is read from."""

    _fields: ClassVar[frozenset[str]] = frozenset(['ahead_of_tariff', 'authority', 'checksum', 'sha256', 'title', 'url'])
    _required: ClassVar[frozenset[str]] = frozenset(['authority'])

    ahead_of_tariff: bool | None
    """True when the duty rests on an official notice (a proclamation, a USTR notice, a customs
    message) that the USITC tariff does not hold yet.
    """

    authority: str
    """Who publishes it: USITC, CBP, USTR, the Federal Register…"""

    checksum: str | None
    """The same SHA-256 as sha256, under the name some sources give it."""

    sha256: str | None
    """SHA-256 of the document as archived: the very copy the rate was read from."""

    title: str | None
    """Its title, or the edition of the tariff. A measure whose text has not changed since
    keeps citing an earlier edition than the publication's.
    """

    url: str | None
    """Where the official document is published: an edition of the tariff at its own file,
    which keeps serving the bytes of sha256. A publication prepared before 2026-11-03 gives
    the address of the current edition instead, whose bytes differ once a later edition is
    out.
    """


class Status(Model):
    """Freshness and verification of the data, and its coverage; the same as the pages /status/
    and /coverage/.
    """

    _fields: ClassVar[frozenset[str]] = frozenset(['coverage', 'engine_version', 'freshness_target_hours', 'frozen', 'incidents', 'notices', 'publications', 'rule_horizon', 'verification'])
    _required: ClassVar[frozenset[str]] = frozenset(['coverage', 'engine_version', 'freshness_target_hours', 'frozen', 'incidents', 'notices', 'publications', 'rule_horizon', 'verification'])

    coverage: dict[str, Any]
    """Chapter 99 positions and their status, the share of estimates withheld, historical
    periods, base rates, agreements, fees and what is out of scope.
    """

    engine_version: str
    """The engine that calculates every estimate now."""

    freshness_target_hours: int
    """Past this age, the sources are stale."""

    frozen: bool
    """True while no new publication may be put in service."""

    incidents: list[dict[str, Any]]
    """Wrong-rate incidents open, notified or corrected: reference, status, notice and
    opened_at.
    """

    notices: list[dict[str, Any]]
    """Positions still in review after the public notice delay: position, since, reason and
    detected_at.
    """

    publications: list[dict[str, Any]]
    """The publications in service, by edition: edition, valid_from, valid_to, publication_id
    and approved_from.
    """

    rule_horizon: dict[str, Any]
    """Until when the fee schedules run (fee_rules_until), and in how many days
    (days_remaining).
    """

    verification: dict[str, Any]
    """Whether the scheduled verification of the sources works: status, last_success,
    last_failure and consecutive_failures, as in a result.
    """


class Verification(Model):
    """Whether the scheduled verification of the official sources works."""

    _fields: ClassVar[frozenset[str]] = frozenset(['consecutive_failures', 'last_failure', 'last_success', 'status'])
    _required: ClassVar[frozenset[str]] = frozenset(['consecutive_failures', 'last_failure', 'last_success', 'status'])

    consecutive_failures: int
    """How many verifications failed in a row, the latest included."""

    last_failure: str | None
    """When it last failed."""

    last_success: str | None
    """When it last worked."""

    status: Literal["healthy", "failing", "unknown"]
    """healthy: the last verification worked. failing: the last ones failed. unknown: none has
    run.
    """
