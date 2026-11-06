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
    """A formal entry pays the merchandise processing fee (MPF) on its value. An informal entry
    pays a fixed fee the estimate does not calculate: it gives no fees.
    """
    facts: Mapping[str, int | float | Decimal | str | bool]
    """Answers to the questions of the facts catalogue (GET /v2/facts), by name. A name that is
    no question is refused, so that a typing error never gives a figure on the ordinary
    case.
    """
    freight: int | float | Decimal | str
    """International freight in US dollars: no duty on it, it adds to the landed cost."""
    include_fees: bool
    """Count the entry fees (MPF, HMF) of a declaration of this product alone. Each product is
    estimated as its own declaration: the MPF is charged once on a declaration, so for
    several products entered together use POST /v2/estimates/entry.
    """
    insurance: int | float | Decimal | str
    """Insurance of the shipment in US dollars: no duty on it, it adds to the landed cost."""
    label: str
    """A name for the saved estimate; needs save."""
    preference: str | None
    """A trade agreement's symbol from the HTS special column (S for USMCA, KR for KORUS…; GET
    /v2/agreements). Giving it declares that the goods meet its rules of origin and that you
    hold the proof.
    """
    quantities: Mapping[str, int | float | Decimal | str]
    """Quantities in the units a duty counts (kg, l, item, dozen, pair, proof_liter…),
    nonnegative. An answer names the quantity it needs in missing ("quantities.kg").
    """
    save: bool
    """Save the estimate: only a saved estimate keeps its detail, is reported, and is notified
    if a rate proves wrong. An answer without a figure is not saved. Send an Idempotency-
    Key: without one, a request sent again after a timeout saves twice.
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
    """Answers to the questions of the facts catalogue (GET /v2/facts), by name. A name that is
    no question is refused, so that a typing error never gives a figure on the ordinary
    case.
    """
    preference: str | None
    """A trade agreement's symbol from the HTS special column (S for USMCA, KR for KORUS…; GET
    /v2/agreements). Giving it declares that the goods meet its rules of origin and that you
    hold the proof.
    """
    quantities: Mapping[str, int | float | Decimal | str]
    """Quantities in the units a duty counts (kg, l, item, dozen, pair, proof_liter…),
    nonnegative. An answer names the quantity it needs in missing ("quantities.kg").
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


class AskedBy(Model):
    """An official text that asks a question: read it to answer precisely."""

    _fields: ClassVar[frozenset[str]] = frozenset(['heading', 'title', 'url'])
    _required: ClassVar[frozenset[str]] = frozenset(['heading', 'title', 'url'])

    heading: str | None
    """The Chapter 99 heading, or the tariff line, whose text asks it; null for a regulation."""

    title: str
    """What it is, in words."""

    url: str
    """Where to read it: the heading's page, with its text and the note it cites, or the
    official document of a notice read ahead of the tariff.
    """


class AuditedDeclaration(Model):
    """A saved declaration's answer, with the detail behind it."""

    _fields: ClassVar[frozenset[str]] = frozenset(['as_of', 'audit', 'data', 'entry_type', 'estimated_duty', 'estimated_duty_rate', 'estimated_fees', 'estimated_landed_cost', 'facts', 'fees', 'freight', 'insurance', 'last_approved', 'lines', 'reference', 'status', 'transport_mode', 'warnings'])
    _required: ClassVar[frozenset[str]] = frozenset(['as_of', 'audit', 'data', 'entry_type', 'lines', 'status', 'transport_mode'])
    _nested: ClassVar[dict[str, Any]] = {'data': 'Data', 'fees': ['EntryFee'], 'last_approved': 'LastApproved', 'lines': ['AuditedLine']}

    as_of: str
    """The day calculated, in New York."""

    audit: dict[str, Any]
    """The detail behind the answer, kept with a saved estimate: the measures examined with the
    decision and the reason of each, every duty and fee in full, the answers supposed and
    what each other answer gives, the sources, the inputs as calculated and the versions.
    """

    data: Data

    entry_type: str | None
    """formal, unless you send informal. An informal entry has no calculated fees."""

    estimated_duty: str | None
    """The duties of every line, in US dollars."""

    estimated_duty_rate: str | None
    """Those duties as a fraction of the values."""

    estimated_fees: str | None
    """The entry fees of the declaration, in US dollars."""

    estimated_landed_cost: str | None
    """Values, duties, fees, freight and insurance, in US dollars."""

    facts: dict[str, Any] | None
    """The exemption its fees rest on, when one was declared for it."""

    fees: list[EntryFee] | None
    """Each entry fee, with its amount and source."""

    freight: str | None
    """The freight you sent, in US dollars."""

    insurance: str | None
    """The insurance you sent, in US dollars."""

    last_approved: LastApproved | None
    """While a duty is withheld, the last result established without it."""

    lines: list[AuditedLine]
    """Each line, in the order sent, with its detail."""

    reference: str | None
    """Your reference for it, when you sent one."""

    status: Literal["calculated", "rate_only", "needs_information", "partial", "unsupported", "not_found", "not_covered"]
    """calculated: every duty is established; without a customs value, a duty that does not
    need it comes with estimated_fees and estimated_landed_cost null, and a warning says so.
    rate_only: no customs value was sent, and estimated_duty_rate is the answer; send the
    value for the amounts. needs_information: something is missing to give a figure, and
    missing says what to send again, on each line of a declaration. partial: a duty is
    withheld for now, and withheld says which; no total is given. unsupported: a regime or a
    rate the service does not calculate. not_found: a code the tariff does not have, or that
    names no product. not_covered: the date or the chapter is outside the data.
    """

    transport_mode: str | None
    """How the goods arrive. Sent, or else supposed: land for Canada and Mexico, ocean
    otherwise. By sea they pay the HMF.
    """

    warnings: list[str] | None
    """What the amounts do not cover, in words."""


class AuditedEstimate(Model):
    """A saved estimate's answer, with the detail behind it."""

    _fields: ClassVar[frozenset[str]] = frozenset(['as_of', 'audit', 'candidates', 'customs_value', 'data', 'description', 'duties', 'entry_type', 'estimated_duty', 'estimated_duty_rate', 'estimated_fees', 'estimated_landed_cost', 'facts', 'fees', 'freight', 'hts', 'insurance', 'last_approved', 'missing', 'origin', 'quantities', 'status', 'transport_mode', 'warnings', 'withheld'])
    _required: ClassVar[frozenset[str]] = frozenset(['as_of', 'audit', 'customs_value', 'data', 'description', 'entry_type', 'hts', 'origin', 'status', 'transport_mode'])
    _nested: ClassVar[dict[str, Any]] = {'candidates': ['Candidate'], 'data': 'Data', 'duties': ['Duty'], 'fees': ['EntryFee'], 'last_approved': 'LastApproved', 'missing': ['MissingField'], 'withheld': ['Withheld']}

    as_of: str
    """The day calculated, in New York."""

    audit: dict[str, Any]
    """The detail behind the answer, kept with a saved estimate: the measures examined with the
    decision and the reason of each, every duty and fee in full, the answers supposed and
    what each other answer gives, the sources, the inputs as calculated and the versions.
    """

    candidates: list[Candidate] | None
    """The longer codes under a short one: send one of them as hts."""

    customs_value: str | None
    """The customs value you sent, in US dollars; null without one."""

    data: Data

    description: str | None
    """What the code covers, in the words of the tariff."""

    duties: list[Duty] | None
    """Each duty, with its rate, amount and source."""

    entry_type: str | None
    """formal, unless you send informal. An informal entry has no calculated fees."""

    estimated_duty: str | None
    """All the duties, in US dollars. Null is unknown, never zero."""

    estimated_duty_rate: str | None
    """The duties as a fraction of the customs value: 0.365 is 36.5%. Without a value, the sum
    of the rates; null when a duty is not a percentage, or while a duty is withheld.
    """

    estimated_fees: str | None
    """All the entry fees, in US dollars; null when one cannot be calculated, or with
    include_fees false.
    """

    estimated_landed_cost: str | None
    """Customs value, duties, fees, freight and insurance, in US dollars; null when the value
    or a fee asked for is not known.
    """

    facts: dict[str, Any] | None
    """The answers this estimate rests on, those you sent and those supposed: the ordinary case
    of each question a rule asks of these goods. Send any of them in facts to change the
    estimate; GET /v2/facts gives each one's question and answers.
    """

    fees: list[EntryFee] | None
    """Each entry fee, with its amount and source."""

    freight: str | None
    """The freight you sent, in US dollars."""

    hts: str
    """The HTS code, in digits."""

    insurance: str | None
    """The insurance you sent, in US dollars."""

    last_approved: LastApproved | None
    """While a duty is withheld, the last result established without it."""

    missing: list[MissingField] | None
    """What to send again for a figure, with status needs_information."""

    origin: str
    """The country of origin."""

    quantities: dict[str, Any] | None
    """The quantities you sent."""

    status: Literal["calculated", "rate_only", "needs_information", "partial", "unsupported", "not_found", "not_covered"]
    """calculated: every duty is established; without a customs value, a duty that does not
    need it comes with estimated_fees and estimated_landed_cost null, and a warning says so.
    rate_only: no customs value was sent, and estimated_duty_rate is the answer; send the
    value for the amounts. needs_information: something is missing to give a figure, and
    missing says what to send again, on each line of a declaration. partial: a duty is
    withheld for now, and withheld says which; no total is given. unsupported: a regime or a
    rate the service does not calculate. not_found: a code the tariff does not have, or that
    names no product. not_covered: the date or the chapter is outside the data.
    """

    transport_mode: str | None
    """How the goods arrive. Sent, or else supposed: land for Canada and Mexico, ocean
    otherwise. By sea they pay the HMF.
    """

    warnings: list[str] | None
    """What the amounts do not cover, in words."""

    withheld: list[Withheld] | None
    """What the total leaves out for now."""


class AuditedLine(Model):
    """One line of a saved declaration, with the detail behind it."""

    _fields: ClassVar[frozenset[str]] = frozenset(['audit', 'candidates', 'customs_value', 'description', 'duties', 'estimated_duty', 'estimated_duty_rate', 'facts', 'hts', 'missing', 'origin', 'quantities', 'reference', 'status', 'warnings', 'withheld'])
    _required: ClassVar[frozenset[str]] = frozenset(['audit', 'customs_value', 'description', 'hts', 'origin', 'status'])
    _nested: ClassVar[dict[str, Any]] = {'candidates': ['Candidate'], 'duties': ['Duty'], 'missing': ['MissingField'], 'withheld': ['Withheld']}

    audit: dict[str, Any]
    """The detail behind the answer, kept with a saved estimate: the measures examined with the
    decision and the reason of each, every duty and fee in full, the answers supposed and
    what each other answer gives, the sources, the inputs as calculated and the versions.
    """

    candidates: list[Candidate] | None
    """The longer codes under a short one: send one of them as hts."""

    customs_value: str | None
    """The customs value you sent, in US dollars; null without one."""

    description: str | None
    """What the code covers, in the words of the tariff."""

    duties: list[Duty] | None
    """Each duty, with its rate, amount and source."""

    estimated_duty: str | None
    """All the duties, in US dollars. Null is unknown, never zero."""

    estimated_duty_rate: str | None
    """The duties as a fraction of the customs value: 0.365 is 36.5%. Without a value, the sum
    of the rates; null when a duty is not a percentage, or while a duty is withheld.
    """

    facts: dict[str, Any] | None
    """The answers this estimate rests on, those you sent and those supposed: the ordinary case
    of each question a rule asks of these goods. Send any of them in facts to change the
    estimate; GET /v2/facts gives each one's question and answers.
    """

    hts: str
    """The HTS code, in digits."""

    missing: list[MissingField] | None
    """What to send again for a figure, with status needs_information."""

    origin: str
    """The country of origin."""

    quantities: dict[str, Any] | None
    """The quantities you sent."""

    reference: str | None
    """Your reference for it, when you sent one."""

    status: Literal["calculated", "rate_only", "needs_information", "partial", "unsupported", "not_found", "not_covered"]
    """calculated: every duty is established; without a customs value, a duty that does not
    need it comes with estimated_fees and estimated_landed_cost null, and a warning says so.
    rate_only: no customs value was sent, and estimated_duty_rate is the answer; send the
    value for the amounts. needs_information: something is missing to give a figure, and
    missing says what to send again, on each line of a declaration. partial: a duty is
    withheld for now, and withheld says which; no total is given. unsupported: a regime or a
    rate the service does not calculate. not_found: a code the tariff does not have, or that
    names no product. not_covered: the date or the chapter is outside the data.
    """

    warnings: list[str] | None
    """What the amounts do not cover, in words."""

    withheld: list[Withheld] | None
    """What the total leaves out for now."""


class BatchFailure(Model):
    """An item of a batch that could not be calculated."""

    _fields: ClassVar[frozenset[str]] = frozenset(['error', 'index'])
    _required: ClassVar[frozenset[str]] = frozenset(['error', 'index'])
    _nested: ClassVar[dict[str, Any]] = {'error': 'Error'}

    error: Error
    """Why."""

    index: int
    """Its position in the batch, from 0."""


class BatchResult(Model):
    """Each item of a batch, in the order sent."""

    _fields: ClassVar[frozenset[str]] = frozenset(['results'])
    _required: ClassVar[frozenset[str]] = frozenset(['results'])
    _nested: ClassVar[dict[str, Any]] = {'results': [('BatchSuccess', 'BatchFailure')]}

    results: list[BatchSuccess | BatchFailure]
    """Each item, its estimate or its error."""


class BatchSuccess(Model):
    """An item of a batch that was calculated."""

    _fields: ClassVar[frozenset[str]] = frozenset(['index', 'result'])
    _required: ClassVar[frozenset[str]] = frozenset(['index', 'result'])
    _nested: ClassVar[dict[str, Any]] = {'result': 'Estimate'}

    index: int
    """Its position in the batch, from 0."""

    result: Estimate
    """Its estimate, as POST /v2/estimates gives it, without last_approved."""


class Candidate(Model):
    """A longer code under a short one."""

    _fields: ClassVar[frozenset[str]] = frozenset(['description', 'hts'])
    _required: ClassVar[frozenset[str]] = frozenset(['description', 'hts'])

    description: str | None
    """What it covers, in the words of the tariff."""

    hts: str
    """The code, in digits."""


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


class Data(Model):
    """The data the answer rests on."""

    _fields: ClassVar[frozenset[str]] = frozenset(['checked_at', 'edition', 'publication_id', 'stale'])
    _required: ClassVar[frozenset[str]] = frozenset(['edition', 'publication_id'])

    checked_at: str | None
    """When the official sources were last checked; null for a past edition."""

    edition: str | None
    """The edition of the US tariff, in words."""

    publication_id: str | None
    """The publication of the rules it was calculated with: send it as publication_id to
    calculate again with the same rules.
    """

    stale: bool | None
    """True when those checks are older than they should be."""


class Declaration(Model):
    """The estimate of a whole import declaration: each line, and its fees once."""

    _fields: ClassVar[frozenset[str]] = frozenset(['as_of', 'data', 'entry_type', 'estimated_duty', 'estimated_duty_rate', 'estimated_fees', 'estimated_landed_cost', 'facts', 'fees', 'freight', 'insurance', 'last_approved', 'lines', 'reference', 'saved_estimate_id', 'status', 'transport_mode', 'warnings'])
    _required: ClassVar[frozenset[str]] = frozenset(['as_of', 'data', 'entry_type', 'lines', 'status', 'transport_mode'])
    _nested: ClassVar[dict[str, Any]] = {'data': 'Data', 'fees': ['EntryFee'], 'last_approved': 'LastApproved', 'lines': ['Line']}

    as_of: str
    """The day calculated, in New York."""

    data: Data

    entry_type: str | None
    """formal, unless you send informal. An informal entry has no calculated fees."""

    estimated_duty: str | None
    """The duties of every line, in US dollars."""

    estimated_duty_rate: str | None
    """Those duties as a fraction of the values."""

    estimated_fees: str | None
    """The entry fees of the declaration, in US dollars."""

    estimated_landed_cost: str | None
    """Values, duties, fees, freight and insurance, in US dollars."""

    facts: dict[str, Any] | None
    """The exemption its fees rest on, when one was declared for it."""

    fees: list[EntryFee] | None
    """Each entry fee, with its amount and source."""

    freight: str | None
    """The freight you sent, in US dollars."""

    insurance: str | None
    """The insurance you sent, in US dollars."""

    last_approved: LastApproved | None
    """While a duty is withheld, the last result established without it."""

    lines: list[Line]
    """Each line, in the order sent."""

    reference: str | None
    """Your reference for it, when you sent one."""

    saved_estimate_id: str | None
    """Sent with save: its identifier, to read it with its detail."""

    status: Literal["calculated", "rate_only", "needs_information", "partial", "unsupported", "not_found", "not_covered"]
    """calculated: every duty is established; without a customs value, a duty that does not
    need it comes with estimated_fees and estimated_landed_cost null, and a warning says so.
    rate_only: no customs value was sent, and estimated_duty_rate is the answer; send the
    value for the amounts. needs_information: something is missing to give a figure, and
    missing says what to send again, on each line of a declaration. partial: a duty is
    withheld for now, and withheld says which; no total is given. unsupported: a regime or a
    rate the service does not calculate. not_found: a code the tariff does not have, or that
    names no product. not_covered: the date or the chapter is outside the data.
    """

    transport_mode: str | None
    """How the goods arrive. Sent, or else supposed: land for Canada and Mexico, ocean
    otherwise. By sea they pay the HMF.
    """

    warnings: list[str] | None
    """What the amounts do not cover, in words."""


class Duty(Model):
    """One duty of the estimate."""

    _fields: ClassVar[frozenset[str]] = frozenset(['amount', 'heading', 'name', 'rate', 'source'])
    _required: ClassVar[frozenset[str]] = frozenset(['amount', 'heading', 'name', 'rate', 'source'])
    _nested: ClassVar[dict[str, Any]] = {'source': 'Source'}

    amount: str | None
    """Its amount in US dollars; null when it cannot be calculated yet."""

    heading: str | None
    """Its Chapter 99 heading; null for the base duty."""

    name: str
    """What the duty is, in words."""

    rate: str | None
    """Its rate, as a person reads it."""

    source: Source | None
    """The official document it rests on."""


class EntryFee(Model):
    """One entry fee of the declaration."""

    _fields: ClassVar[frozenset[str]] = frozenset(['amount', 'name', 'note', 'source'])
    _required: ClassVar[frozenset[str]] = frozenset(['amount', 'name', 'source'])
    _nested: ClassVar[dict[str, Any]] = {'source': 'Source'}

    amount: str | None
    """Its amount in US dollars; null when it cannot be calculated yet."""

    name: str
    """What the fee is, in words: the merchandise processing fee (MPF) or the harbor
    maintenance fee (HMF).
    """

    note: str | None
    """Why its amount is what it is, when that needs saying."""

    source: Source | None
    """The official document it rests on."""


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


class Estimate(Model):
    """The estimate of one product."""

    _fields: ClassVar[frozenset[str]] = frozenset(['as_of', 'candidates', 'customs_value', 'data', 'description', 'duties', 'entry_type', 'estimated_duty', 'estimated_duty_rate', 'estimated_fees', 'estimated_landed_cost', 'facts', 'fees', 'freight', 'hts', 'insurance', 'last_approved', 'missing', 'origin', 'quantities', 'saved_estimate_id', 'status', 'transport_mode', 'warnings', 'withheld'])
    _required: ClassVar[frozenset[str]] = frozenset(['as_of', 'customs_value', 'data', 'description', 'entry_type', 'hts', 'origin', 'status', 'transport_mode'])
    _nested: ClassVar[dict[str, Any]] = {'candidates': ['Candidate'], 'data': 'Data', 'duties': ['Duty'], 'fees': ['EntryFee'], 'last_approved': 'LastApproved', 'missing': ['MissingField'], 'withheld': ['Withheld']}

    as_of: str
    """The day calculated, in New York."""

    candidates: list[Candidate] | None
    """The longer codes under a short one: send one of them as hts."""

    customs_value: str | None
    """The customs value you sent, in US dollars; null without one."""

    data: Data

    description: str | None
    """What the code covers, in the words of the tariff."""

    duties: list[Duty] | None
    """Each duty, with its rate, amount and source."""

    entry_type: str | None
    """formal, unless you send informal. An informal entry has no calculated fees."""

    estimated_duty: str | None
    """All the duties, in US dollars. Null is unknown, never zero."""

    estimated_duty_rate: str | None
    """The duties as a fraction of the customs value: 0.365 is 36.5%. Without a value, the sum
    of the rates; null when a duty is not a percentage, or while a duty is withheld.
    """

    estimated_fees: str | None
    """All the entry fees, in US dollars; null when one cannot be calculated, or with
    include_fees false.
    """

    estimated_landed_cost: str | None
    """Customs value, duties, fees, freight and insurance, in US dollars; null when the value
    or a fee asked for is not known.
    """

    facts: dict[str, Any] | None
    """The answers this estimate rests on, those you sent and those supposed: the ordinary case
    of each question a rule asks of these goods. Send any of them in facts to change the
    estimate; GET /v2/facts gives each one's question and answers.
    """

    fees: list[EntryFee] | None
    """Each entry fee, with its amount and source."""

    freight: str | None
    """The freight you sent, in US dollars."""

    hts: str
    """The HTS code, in digits."""

    insurance: str | None
    """The insurance you sent, in US dollars."""

    last_approved: LastApproved | None
    """While a duty is withheld, the last result established without it."""

    missing: list[MissingField] | None
    """What to send again for a figure, with status needs_information."""

    origin: str
    """The country of origin."""

    quantities: dict[str, Any] | None
    """The quantities you sent."""

    saved_estimate_id: str | None
    """Sent with save: its identifier, to read it with its detail."""

    status: Literal["calculated", "rate_only", "needs_information", "partial", "unsupported", "not_found", "not_covered"]
    """calculated: every duty is established; without a customs value, a duty that does not
    need it comes with estimated_fees and estimated_landed_cost null, and a warning says so.
    rate_only: no customs value was sent, and estimated_duty_rate is the answer; send the
    value for the amounts. needs_information: something is missing to give a figure, and
    missing says what to send again, on each line of a declaration. partial: a duty is
    withheld for now, and withheld says which; no total is given. unsupported: a regime or a
    rate the service does not calculate. not_found: a code the tariff does not have, or that
    names no product. not_covered: the date or the chapter is outside the data.
    """

    transport_mode: str | None
    """How the goods arrive. Sent, or else supposed: land for Canada and Mexico, ocean
    otherwise. By sea they pay the HMF.
    """

    warnings: list[str] | None
    """What the amounts do not cover, in words."""

    withheld: list[Withheld] | None
    """What the total leaves out for now."""


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

    _fields: ClassVar[frozenset[str]] = frozenset(['asked_by', 'choices', 'default', 'help', 'name', 'question', 'scope', 'type', 'unit'])
    _required: ClassVar[frozenset[str]] = frozenset(['help', 'name', 'question', 'scope', 'type'])
    _nested: ClassVar[dict[str, Any]] = {'asked_by': ['AskedBy'], 'choices': ['FactChoice']}
    _defaults: ClassVar[dict[str, Any]] = {'asked_by': [], 'choices': [], 'unit': ''}

    asked_by: list[AskedBy]
    """The official texts that ask it today: the headings whose rules in service read it, or
    the regulation of a fee. Empty for what depends on each product's own line (its rate,
    its entry); an estimate names, in missing, those that ask it for its goods.
    """

    choices: list[FactChoice]
    """For a choice: the values to choose from."""

    default: Any
    """The ordinary case, supposed when unanswered."""

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
    dollars), number or country (ISO code).
    """

    unit: str
    """The unit of a number, if any."""


class FactList(Model):
    """The questions an estimate may ask."""

    _fields: ClassVar[frozenset[str]] = frozenset(['facts'])
    _required: ClassVar[frozenset[str]] = frozenset(['facts'])
    _nested: ClassVar[dict[str, Any]] = {'facts': ['FactDefinition']}

    facts: list[FactDefinition]
    """The questions that can change an answer today."""


class HistoryPoint(Model):
    """The product at one change of the tariff."""

    _fields: ClassVar[frozenset[str]] = frozenset(['as_of', 'candidates', 'customs_value', 'data', 'description', 'duties', 'entry_type', 'estimated_duty', 'estimated_duty_rate', 'estimated_fees', 'estimated_landed_cost', 'facts', 'fees', 'freight', 'hts', 'insurance', 'known_ieepa_duty', 'last_approved', 'missing', 'origin', 'quantities', 'status', 'transport_mode', 'warnings', 'withheld'])
    _required: ClassVar[frozenset[str]] = frozenset(['as_of', 'customs_value', 'data', 'description', 'entry_type', 'hts', 'origin', 'status', 'transport_mode'])
    _nested: ClassVar[dict[str, Any]] = {'candidates': ['Candidate'], 'data': 'Data', 'duties': ['Duty'], 'fees': ['EntryFee'], 'last_approved': 'LastApproved', 'missing': ['MissingField'], 'withheld': ['Withheld']}

    as_of: str
    """The day calculated, in New York."""

    candidates: list[Candidate] | None
    """The longer codes under a short one: send one of them as hts."""

    customs_value: str | None
    """The customs value you sent, in US dollars; null without one."""

    data: Data

    description: str | None
    """What the code covers, in the words of the tariff."""

    duties: list[Duty] | None
    """Each duty, with its rate, amount and source."""

    entry_type: str | None
    """formal, unless you send informal. An informal entry has no calculated fees."""

    estimated_duty: str | None
    """All the duties, in US dollars. Null is unknown, never zero."""

    estimated_duty_rate: str | None
    """The duties as a fraction of the customs value: 0.365 is 36.5%. Without a value, the sum
    of the rates; null when a duty is not a percentage, or while a duty is withheld.
    """

    estimated_fees: str | None
    """All the entry fees, in US dollars; null when one cannot be calculated, or with
    include_fees false.
    """

    estimated_landed_cost: str | None
    """Customs value, duties, fees, freight and insurance, in US dollars; null when the value
    or a fee asked for is not known.
    """

    facts: dict[str, Any] | None
    """The answers this estimate rests on, those you sent and those supposed: the ordinary case
    of each question a rule asks of these goods. Send any of them in facts to change the
    estimate; GET /v2/facts gives each one's question and answers.
    """

    fees: list[EntryFee] | None
    """Each entry fee, with its amount and source."""

    freight: str | None
    """The freight you sent, in US dollars."""

    hts: str
    """The HTS code, in digits."""

    insurance: str | None
    """The insurance you sent, in US dollars."""

    known_ieepa_duty: str | None
    """What the IEEPA duties amount to that day, in US dollars; null when not established."""

    last_approved: LastApproved | None
    """While a duty is withheld, the last result established without it."""

    missing: list[MissingField] | None
    """What to send again for a figure, with status needs_information."""

    origin: str
    """The country of origin."""

    quantities: dict[str, Any] | None
    """The quantities you sent."""

    status: Literal["calculated", "rate_only", "needs_information", "partial", "unsupported", "not_found", "not_covered"]
    """calculated: every duty is established; without a customs value, a duty that does not
    need it comes with estimated_fees and estimated_landed_cost null, and a warning says so.
    rate_only: no customs value was sent, and estimated_duty_rate is the answer; send the
    value for the amounts. needs_information: something is missing to give a figure, and
    missing says what to send again, on each line of a declaration. partial: a duty is
    withheld for now, and withheld says which; no total is given. unsupported: a regime or a
    rate the service does not calculate. not_found: a code the tariff does not have, or that
    names no product. not_covered: the date or the chapter is outside the data.
    """

    transport_mode: str | None
    """How the goods arrive. Sent, or else supposed: land for Canada and Mexico, ocean
    otherwise. By sea they pay the HMF.
    """

    warnings: list[str] | None
    """What the amounts do not cover, in words."""

    withheld: list[Withheld] | None
    """What the total leaves out for now."""


class HistoryResult(Model):
    """The product at every change of the tariff over the period."""

    _fields: ClassVar[frozenset[str]] = frozenset(['covered_windows', 'points'])
    _required: ClassVar[frozenset[str]] = frozenset(['covered_windows', 'points'])
    _nested: ClassVar[dict[str, Any]] = {'covered_windows': ['CoveredWindow'], 'points': ['HistoryPoint']}

    covered_windows: list[CoveredWindow]
    """The periods the data covers, by publication."""

    points: list[HistoryPoint]
    """The product at each change, in order of date."""


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


class LastApproved(Model):
    """The last result established without what is withheld now: dated, kept apart, in no
    total.
    """

    _fields: ClassVar[frozenset[str]] = frozenset(['approved_from', 'approved_to', 'as_of', 'edition', 'estimated_duty', 'estimated_landed_cost', 'publication_id', 'status'])
    _required: ClassVar[frozenset[str]] = frozenset(['approved_from', 'approved_to', 'as_of', 'edition', 'estimated_duty', 'estimated_landed_cost', 'publication_id', 'status'])

    approved_from: str | None
    """When that publication went into service."""

    approved_to: str | None
    """When it left service; null while it serves."""

    as_of: str | None
    """The day it was calculated for."""

    edition: str | None
    """The edition of the US tariff, in words."""

    estimated_duty: str | None
    """Its duty then, in US dollars."""

    estimated_landed_cost: str | None
    """Its landed cost then, in US dollars."""

    publication_id: str | None
    """The publication of the rules it was calculated with: send it as publication_id to
    calculate again with the same rules.
    """

    status: Literal["calculated", "rate_only", "needs_information", "partial", "unsupported", "not_found", "not_covered"]
    """Its status then."""


class Line(Model):
    """One line of a declaration: its fees are the declaration's."""

    _fields: ClassVar[frozenset[str]] = frozenset(['candidates', 'customs_value', 'description', 'duties', 'estimated_duty', 'estimated_duty_rate', 'facts', 'hts', 'missing', 'origin', 'quantities', 'reference', 'status', 'warnings', 'withheld'])
    _required: ClassVar[frozenset[str]] = frozenset(['customs_value', 'description', 'hts', 'origin', 'status'])
    _nested: ClassVar[dict[str, Any]] = {'candidates': ['Candidate'], 'duties': ['Duty'], 'missing': ['MissingField'], 'withheld': ['Withheld']}

    candidates: list[Candidate] | None
    """The longer codes under a short one: send one of them as hts."""

    customs_value: str | None
    """The customs value you sent, in US dollars; null without one."""

    description: str | None
    """What the code covers, in the words of the tariff."""

    duties: list[Duty] | None
    """Each duty, with its rate, amount and source."""

    estimated_duty: str | None
    """All the duties, in US dollars. Null is unknown, never zero."""

    estimated_duty_rate: str | None
    """The duties as a fraction of the customs value: 0.365 is 36.5%. Without a value, the sum
    of the rates; null when a duty is not a percentage, or while a duty is withheld.
    """

    facts: dict[str, Any] | None
    """The answers this estimate rests on, those you sent and those supposed: the ordinary case
    of each question a rule asks of these goods. Send any of them in facts to change the
    estimate; GET /v2/facts gives each one's question and answers.
    """

    hts: str
    """The HTS code, in digits."""

    missing: list[MissingField] | None
    """What to send again for a figure, with status needs_information."""

    origin: str
    """The country of origin."""

    quantities: dict[str, Any] | None
    """The quantities you sent."""

    reference: str | None
    """Your reference for it, when you sent one."""

    status: Literal["calculated", "rate_only", "needs_information", "partial", "unsupported", "not_found", "not_covered"]
    """calculated: every duty is established; without a customs value, a duty that does not
    need it comes with estimated_fees and estimated_landed_cost null, and a warning says so.
    rate_only: no customs value was sent, and estimated_duty_rate is the answer; send the
    value for the amounts. needs_information: something is missing to give a figure, and
    missing says what to send again, on each line of a declaration. partial: a duty is
    withheld for now, and withheld says which; no total is given. unsupported: a regime or a
    rate the service does not calculate. not_found: a code the tariff does not have, or that
    names no product. not_covered: the date or the chapter is outside the data.
    """

    warnings: list[str] | None
    """What the amounts do not cover, in words."""

    withheld: list[Withheld] | None
    """What the total leaves out for now."""


class MissingField(Model):
    """What the service needs to give a figure."""

    _fields: ClassVar[frozenset[str]] = frozenset(['asked_by', 'choices', 'field', 'question', 'type', 'unit'])
    _required: ClassVar[frozenset[str]] = frozenset(['field', 'question', 'type'])
    _nested: ClassVar[dict[str, Any]] = {'asked_by': ['AskedBy']}

    asked_by: list[AskedBy] | None
    """The official texts that ask it for these goods, to answer it precisely."""

    choices: list[Any] | None
    """The values a choice takes."""

    field: str
    """Where to send it in the request."""

    question: str
    """What it asks, in words."""

    type: str
    """The type of its value: number, money, boolean, choice, text, country or datetime."""

    unit: str | None
    """The unit of a quantity."""


class SavedDetail(Model):
    """A saved estimate, with the detail behind its answer."""

    _fields: ClassVar[frozenset[str]] = frozenset(['author', 'created_at', 'estimated_duty', 'id', 'incidents', 'inputs', 'kind', 'label', 'publication_id', 'result', 'source', 'status'])
    _required: ClassVar[frozenset[str]] = frozenset(['author', 'created_at', 'estimated_duty', 'id', 'incidents', 'inputs', 'kind', 'label', 'publication_id', 'result', 'source', 'status'])
    _nested: ClassVar[dict[str, Any]] = {'incidents': ['SavedIncident'], 'result': ('AuditedEstimate', 'AuditedDeclaration')}

    author: str
    """Who saved it."""

    created_at: str
    """When it was saved."""

    estimated_duty: str | None
    """All the duties, in US dollars."""

    id: str
    """Its identifier."""

    incidents: list[SavedIncident]
    """The incidents found since that concern it."""

    inputs: dict[str, Any]
    """The request as calculated: its date, publication and answers."""

    kind: Literal["single", "entry"]
    """single: one product. entry: a declaration."""

    label: str
    """The name it was given."""

    publication_id: str | None
    """The publication of the rules it was calculated with: send it as publication_id to
    calculate again with the same rules.
    """

    result: AuditedEstimate | AuditedDeclaration
    """Its answer and its detail."""

    source: str
    """Where it was saved: api, mcp, portal or import."""

    status: Literal["calculated", "rate_only", "needs_information", "partial", "unsupported", "not_found", "not_covered"]
    """calculated: every duty is established; without a customs value, a duty that does not
    need it comes with estimated_fees and estimated_landed_cost null, and a warning says so.
    rate_only: no customs value was sent, and estimated_duty_rate is the answer; send the
    value for the amounts. needs_information: something is missing to give a figure, and
    missing says what to send again, on each line of a declaration. partial: a duty is
    withheld for now, and withheld says which; no total is given. unsupported: a regime or a
    rate the service does not calculate. not_found: a code the tariff does not have, or that
    names no product. not_covered: the date or the chapter is outside the data.
    """


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
    """A page of saved estimates, the newest first."""

    _fields: ClassVar[frozenset[str]] = frozenset(['count', 'limit', 'offset', 'results'])
    _required: ClassVar[frozenset[str]] = frozenset(['count', 'limit', 'offset', 'results'])
    _nested: ClassVar[dict[str, Any]] = {'results': ['SavedSummary']}

    count: int
    """How many there are in all."""

    limit: int
    """How many were asked."""

    offset: int
    """How many were skipped."""

    results: list[SavedSummary]
    """This page."""


class SavedSummary(Model):
    """A saved estimate in a list."""

    _fields: ClassVar[frozenset[str]] = frozenset(['author', 'created_at', 'estimated_duty', 'id', 'incidents', 'kind', 'label', 'publication_id', 'source', 'status'])
    _required: ClassVar[frozenset[str]] = frozenset(['author', 'created_at', 'estimated_duty', 'id', 'incidents', 'kind', 'label', 'publication_id', 'source', 'status'])
    _nested: ClassVar[dict[str, Any]] = {'incidents': ['SavedIncident']}

    author: str
    """Who saved it."""

    created_at: str
    """When it was saved."""

    estimated_duty: str | None
    """All the duties, in US dollars."""

    id: str
    """Its identifier."""

    incidents: list[SavedIncident]
    """The incidents found since that concern it."""

    kind: Literal["single", "entry"]
    """single: one product. entry: a declaration."""

    label: str
    """The name it was given."""

    publication_id: str | None
    """The publication of the rules it was calculated with: send it as publication_id to
    calculate again with the same rules.
    """

    source: str
    """Where it was saved: api, mcp, portal or import."""

    status: Literal["calculated", "rate_only", "needs_information", "partial", "unsupported", "not_found", "not_covered"]
    """calculated: every duty is established; without a customs value, a duty that does not
    need it comes with estimated_fees and estimated_landed_cost null, and a warning says so.
    rate_only: no customs value was sent, and estimated_duty_rate is the answer; send the
    value for the amounts. needs_information: something is missing to give a figure, and
    missing says what to send again, on each line of a declaration. partial: a duty is
    withheld for now, and withheld says which; no total is given. unsupported: a regime or a
    rate the service does not calculate. not_found: a code the tariff does not have, or that
    names no product. not_covered: the date or the chapter is outside the data.
    """


class Source(Model):
    """The official document an amount rests on."""

    _fields: ClassVar[frozenset[str]] = frozenset(['sha256', 'title', 'url'])
    _required: ClassVar[frozenset[str]] = frozenset(['sha256', 'title', 'url'])

    sha256: str | None
    """The SHA-256 of the file, to check it is the one cited."""

    title: str | None
    """Its title."""

    url: str | None
    """Where to read it: the file of that edition."""


class Status(Model):
    """Whether the data can be relied on now, and which data answers. The pages /status/ and
    /coverage/ say more.
    """

    _fields: ClassVar[frozenset[str]] = frozenset(['checked_at', 'covered_from', 'edition', 'engine_version', 'incidents', 'publication_id', 'stale', 'status'])
    _required: ClassVar[frozenset[str]] = frozenset(['checked_at', 'covered_from', 'edition', 'engine_version', 'incidents', 'publication_id', 'stale', 'status'])
    _nested: ClassVar[dict[str, Any]] = {'incidents': ['StatusIncident']}

    checked_at: str | None
    """When the official sources were last checked."""

    covered_from: str | None
    """The first day an estimate can be dated."""

    edition: str | None
    """The edition of the US tariff, in words."""

    engine_version: str
    """The engine that calculates every estimate now."""

    incidents: list[StatusIncident]
    """The wrong rates being corrected."""

    publication_id: str | None
    """The publication of the rules in service. When it changes, or the engine does, an
    estimate you kept may give another result.
    """

    stale: bool
    """True when those checks are older than they should be."""

    status: Literal["ok", "degraded"]
    """ok: the official sources were verified lately. degraded: they could not be: estimates
    still answer, from the data last verified.
    """


class StatusIncident(Model):
    """A wrong rate being corrected."""

    _fields: ClassVar[frozenset[str]] = frozenset(['notice', 'opened_at', 'reference', 'status'])
    _required: ClassVar[frozenset[str]] = frozenset(['notice', 'opened_at', 'reference', 'status'])

    notice: str
    """What is being corrected, in words."""

    opened_at: str
    """When it was opened."""

    reference: str
    """The incident, as the emails and the status page name it."""

    status: str
    """Where it stands: open, notified or corrected."""


class Withheld(Model):
    """What the total leaves out for now."""

    _fields: ClassVar[frozenset[str]] = frozenset(['heading', 'name', 'reason'])
    _required: ClassVar[frozenset[str]] = frozenset(['heading', 'name', 'reason'])

    heading: str | None
    """Its Chapter 99 heading, if any."""

    name: str
    """What is withheld, in words."""

    reason: str
    """Why, and what it means for the total."""
