"""The operations of the TariffTrust API, as methods. Generated from openapi.json by scripts/generate.py: do not edit."""


from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import date, datetime
from decimal import Decimal
from typing import Any, Literal, TypeVar
from urllib.parse import quote

from ._model import Model
from .types import (
    AgreementList,
    BatchItem,
    BatchResult,
    CalculationResult,
    EntryInput,
    EntryResult,
    EstimateInput,
    FactList,
    HistoryResult,
    HtsDetail,
    HtsSearch,
    LineInput,
    Saved,
    SavedDetail,
    SavedList,
    Status,
)

_M = TypeVar("_M", bound=Model)


class Operations:
    """Each operation of the contract, under its operationId."""

    def _request(
        self,
        method: str,
        path: str,
        *,
        model: type[_M],
        query: Mapping[str, Any] | None = None,
        body: Mapping[str, Any] | None = None,
        auth: bool = True,
        idempotent: bool = False,
        idempotency_key: str | None = None,
    ) -> _M:
        raise NotImplementedError

    def list_agreements(
        self,
    ) -> AgreementList:
        """List the trade agreements.

        The agreements the engine applies, by the symbol of the HTS special column, with the
        origins each can apply to. A symbol does not establish eligibility: send it as
        preference, which declares the rules of origin met. Needs the read permission; not
        counted.
        """
        return self._request(
            "GET",
            "/v1/agreements",
            model=AgreementList,
        )

    def estimate(
        self,
        *,
        hts: str,
        origin: str,
        as_of: str | date | datetime | None = None,
        customs_value: int | float | Decimal | str | None = None,
        entry_type: Literal["formal", "informal"] | None = None,
        facts: Mapping[str, int | float | Decimal | str | bool] | None = None,
        freight: int | float | Decimal | str | None = None,
        include_fees: bool | None = None,
        insurance: int | float | Decimal | str | None = None,
        preference: str | None = None,
        publication_id: str | None = None,
        quantities: Mapping[str, int | float | Decimal | str] | None = None,
        transport_mode: Literal["air", "ocean", "land"] | None = None,
        idempotency_key: str | None = None,
    ) -> CalculationResult:
        """Estimate one product.

        Every US duty and fee that applies to one product at a date, each with its official
        source. Without a customs value, the duty rate. Not saved: an unsaved estimate cannot be
        replayed, reported or notified in an incident; save it with POST /v1/saved-estimates.
        Needs the calculate permission; counted in the quota unless it gives no figure of the
        duty: a question asked without any duty amount or rate (status needs_information), a
        code the tariff does not have or that names no product, a regime the service does not
        calculate. A question that gives the duty of each answer (scenarios), their bounds or
        the subtotal already known is counted.

        Args:
            hts: The HTS code of the goods: 4, 6, 8 or 10 digits, dots and spaces ignored. A
                rate needs the 10-digit statistical line or its 8-digit subheading.
            origin: Country of origin: where the goods were produced, not where they ship from.
                ISO 3166-1 alpha-2 (XK for Kosovo), or a code U.S. Customs files with (BU, GZ,
                KV, WE).
            as_of: When the goods are entered for consumption. A day, in New York time
                ("2026-04-05"); or, on a day when a measure takes effect at a stated hour, the
                instant of entry with its UTC offset ("2026-04-05T00:01:00-04:00"). Unset:
                today.
            customs_value: Customs value in US dollars: the transaction value declared, not a
                retail price. Unset: the duty rate is given, and an amount only where the duty
                does not depend on the value.
            entry_type: A formal entry pays the merchandise processing fee (MPF) on its value;
                an informal one, the fixed informal fee.
            facts: Answers to the questions of the facts catalogue (GET /v1/facts), by name. A
                name outside the catalogue is reported in the result and never used.
            freight: International freight in US dollars: no duty on it, it adds to the landed
                cost.
            include_fees: Count the entry fees (MPF, HMF) of a declaration of this product
                alone; the landed cost includes them only then. The MPF is charged once on a
                declaration: for several products entered together, use POST
                /v1/estimates/entry.
            insurance: Insurance of the shipment in US dollars: no duty on it, it adds to the
                landed cost.
            preference: A trade agreement's symbol from the HTS special column (S for USMCA, KR
                for KORUS…; GET /v1/agreements). Giving it declares that the goods meet its
                rules of origin and that you hold the proof.
            publication_id: Calculate with this publication of the rules rather than the one in
                force on the date: a saved result's publication_id replays it.
            quantities: Quantities in the units a duty counts (kg, l, item, dozen, pair,
                proof_liter…), nonnegative. A result names the quantity it needs in
                required_fields ("quantities.kg").
            transport_mode: How the goods arrive; by sea they also pay the harbor maintenance
                fee (HMF). Unset: land for goods of Canada or Mexico, ocean otherwise.
            idempotency_key: Makes a retry of this call safe; a new one is generated for each
                call otherwise.
        """
        return self._request(
            "POST",
            "/v1/estimates",
            model=CalculationResult,
            body={"hts": hts, "origin": origin, "as_of": as_of, "customs_value": customs_value, "entry_type": entry_type, "facts": facts, "freight": freight, "include_fees": include_fees, "insurance": insurance, "preference": preference, "publication_id": publication_id, "quantities": quantities, "transport_mode": transport_mode},
            idempotent=True,
            idempotency_key=idempotency_key,
        )

    def estimate_batch(
        self,
        *,
        items: Sequence[BatchItem],
        publication_id: str | None = None,
        idempotency_key: str | None = None,
    ) -> BatchResult:
        """Estimate up to 200 products.

        Each item calculated on its own, as POST /v1/estimates would, in the order given. An
        invalid item refuses the whole batch (422, error.fields naming items.<index>.<field>);
        an item that cannot be calculated (a date no edition covers) has its own error in
        results, the others are calculated. The batch's publication_id, if any, holds for every
        item. Counted as one request, whatever its number of items, unless none of them gives a
        figure of the duty (questions without any duty amount or rate, and errors, only). When
        the data is unavailable for every item, the batch is a 503 to send again, neither
        counted nor kept for its Idempotency-Key; when only for some, they have their error
        (data_unavailable) in results: send those items again.

        Args:
            items: The products, each calculated on its own.
            publication_id: Calculate with this publication of the rules rather than the one in
                force on the date: a saved result's publication_id replays it.
            idempotency_key: Makes a retry of this call safe; a new one is generated for each
                call otherwise.
        """
        return self._request(
            "POST",
            "/v1/estimates/batch",
            model=BatchResult,
            body={"items": items, "publication_id": publication_id},
            idempotent=True,
            idempotency_key=idempotency_key,
        )

    def estimate_entry(
        self,
        *,
        lines: Sequence[LineInput],
        as_of: str | date | datetime | None = None,
        entry_type: Literal["formal", "informal"] | None = None,
        facts: Mapping[str, int | float | Decimal | str | bool] | None = None,
        freight: int | float | Decimal | str | None = None,
        include_fees: bool | None = None,
        insurance: int | float | Decimal | str | None = None,
        publication_id: str | None = None,
        reference: str | None = None,
        transport_mode: Literal["air", "ocean", "land"] | None = None,
        idempotency_key: str | None = None,
    ) -> EntryResult:
        """Estimate a whole import declaration.

        Every line, then the MPF and the HMF once on the declaration: adding the estimates of
        the lines of one declaration gives a wrong MPF. Not saved: save it with POST /v1/saved-
        estimates (entry) to replay or report it. Counted as one request, whatever its number of
        lines, unless it gives no figure of the duty (a question without any duty amount or
        rate).

        Args:
            lines: The lines of the declaration, each a product.
            as_of: When the goods are entered for consumption. A day, in New York time
                ("2026-04-05"); or, on a day when a measure takes effect at a stated hour, the
                instant of entry with its UTC offset ("2026-04-05T00:01:00-04:00"). Unset:
                today.
            entry_type: A formal entry pays the merchandise processing fee (MPF) on its value;
                an informal one, the fixed informal fee.
            facts: Answers that hold for the whole declaration (GET /v1/facts, scope entry or
                shipment).
            freight: International freight in US dollars: no duty on it, it adds to the landed
                cost.
            include_fees: Count the entry fees (MPF, HMF) of the declaration.
            insurance: Insurance of the shipment in US dollars: no duty on it, it adds to the
                landed cost.
            publication_id: Calculate with this publication of the rules rather than the one in
                force on the date: a saved result's publication_id replays it.
            reference: Your reference for the declaration.
            transport_mode: How the goods arrive; by sea they also pay the harbor maintenance
                fee (HMF). Unset: land for goods of Canada or Mexico, ocean otherwise.
            idempotency_key: Makes a retry of this call safe; a new one is generated for each
                call otherwise.
        """
        return self._request(
            "POST",
            "/v1/estimates/entry",
            model=EntryResult,
            body={"lines": lines, "as_of": as_of, "entry_type": entry_type, "facts": facts, "freight": freight, "include_fees": include_fees, "insurance": insurance, "publication_id": publication_id, "reference": reference, "transport_mode": transport_mode},
            idempotent=True,
            idempotency_key=idempotency_key,
        )

    def estimate_history(
        self,
        *,
        hts: str,
        origin: str,
        customs_value: int | float | Decimal | str | None = None,
        entry_type: Literal["formal", "informal"] | None = None,
        facts: Mapping[str, int | float | Decimal | str | bool] | None = None,
        freight: int | float | Decimal | str | None = None,
        from_: str | date | None = None,
        include_fees: bool | None = None,
        insurance: int | float | Decimal | str | None = None,
        preference: str | None = None,
        quantities: Mapping[str, int | float | Decimal | str] | None = None,
        through: str | date | None = None,
        transport_mode: Literal["air", "ocean", "land"] | None = None,
        idempotency_key: str | None = None,
    ) -> HistoryResult:
        """Estimate one product at every change of the tariff.

        The product calculated on each first day of an edition, on each day a measure or a fee
        that covers it begins or ends, and on each day an incident or a notice not yet read
        begins or stops withholding its estimate, over the period asked, with the rules approved
        today. Counted as one request, whatever its number of points, unless no point gives a
        figure of the duty (a question without any duty amount or rate).

        Args:
            hts: The HTS code of the goods: 4, 6, 8 or 10 digits, dots and spaces ignored. A
                rate needs the 10-digit statistical line or its 8-digit subheading.
            origin: Country of origin: where the goods were produced, not where they ship from.
                ISO 3166-1 alpha-2 (XK for Kosovo), or a code U.S. Customs files with (BU, GZ,
                KV, WE).
            customs_value: Customs value in US dollars: the transaction value declared, not a
                retail price. Unset: the duty rate is given, and an amount only where the duty
                does not depend on the value.
            entry_type: A formal entry pays the merchandise processing fee (MPF) on its value;
                an informal one, the fixed informal fee.
            facts: Answers to the questions of the facts catalogue (GET /v1/facts), by name. A
                name outside the catalogue is reported in the result and never used.
            freight: International freight in US dollars: no duty on it, it adds to the landed
                cost.
            from_: First day of the period. Unset: the first edition the service holds.
            include_fees: Count the entry fees (MPF, HMF) of a declaration of this product
                alone; the landed cost includes them only then. The MPF is charged once on a
                declaration: for several products entered together, use POST
                /v1/estimates/entry.
            insurance: Insurance of the shipment in US dollars: no duty on it, it adds to the
                landed cost.
            preference: A trade agreement's symbol from the HTS special column (S for USMCA, KR
                for KORUS…; GET /v1/agreements). Giving it declares that the goods meet its
                rules of origin and that you hold the proof.
            quantities: Quantities in the units a duty counts (kg, l, item, dozen, pair,
                proof_liter…), nonnegative. A result names the quantity it needs in
                required_fields ("quantities.kg").
            through: Last day of the period, at most today. Unset: today.
            transport_mode: How the goods arrive; by sea they also pay the harbor maintenance
                fee (HMF). Unset: land for goods of Canada or Mexico, ocean otherwise.
            idempotency_key: Makes a retry of this call safe; a new one is generated for each
                call otherwise.
        """
        return self._request(
            "POST",
            "/v1/estimates/history",
            model=HistoryResult,
            body={"hts": hts, "origin": origin, "customs_value": customs_value, "entry_type": entry_type, "facts": facts, "freight": freight, "from": from_, "include_fees": include_fees, "insurance": insurance, "preference": preference, "quantities": quantities, "through": through, "transport_mode": transport_mode},
            idempotent=True,
            idempotency_key=idempotency_key,
        )

    def list_facts(
        self,
    ) -> FactList:
        """List the questions an estimate may ask.

        The facts catalogue: each question a measure may depend on, by the name to answer it
        with in facts, its type, its choices and its ordinary case. A result lists the ones it
        needs in input_guidance, and those it assumed in assumptions. Needs the read permission;
        not counted.
        """
        return self._request(
            "GET",
            "/v1/facts",
            model=FactList,
        )

    def search_hts(
        self,
        *,
        q: str | None = None,
        chapter: str | None = None,
        offset: int | None = None,
        limit: int | None = None,
    ) -> HtsSearch:
        """Search the US tariff schedule.

        The lines of the edition in service whose code starts with q, or whose descriptions hold
        every word of q, in code order; chapter (two digits) narrows them. A match is no
        classification. Needs the read permission; not counted.

        Args:
            q: A code, or words of the descriptions: 200 characters at most.
            chapter: Two digits, as 61: the lines of that chapter only.
            offset: How many lines to skip, from 0 to 100000.
            limit: How many lines to return, from 1 to 100.
        """
        return self._request(
            "GET",
            "/v1/hts",
            model=HtsSearch,
            query={"q": q, "chapter": chapter, "offset": offset, "limit": limit},
        )

    def get_hts(
        self,
        code: str,
    ) -> HtsDetail:
        """Read one line of the US tariff schedule.

        One line of the edition in service: its descriptions, its rate columns and its units.
        Needs the read permission; not counted.

        Args:
            code: An HTS code of 4, 6, 8 or 10 digits, with or without its dots.
        """
        return self._request(
            "GET",
            f"/v1/hts/{quote(code, safe='')}",
            model=HtsDetail,
        )

    def list_saved_estimates(
        self,
        *,
        offset: int | None = None,
        limit: int | None = None,
    ) -> SavedList:
        """List the saved estimates.

        The workspace's saved estimates, the latest first, saved from the API, the MCP or the
        portal. Needs the read permission; not counted.

        Args:
            offset: How many saved estimates to skip.
            limit: How many saved estimates to return, from 1 to 100.
        """
        return self._request(
            "GET",
            "/v1/saved-estimates",
            model=SavedList,
            query={"offset": offset, "limit": limit},
        )

    def save_estimate(
        self,
        *,
        entry: EntryInput | None = None,
        estimate: EstimateInput | None = None,
        label: str | None = None,
        idempotency_key: str | None = None,
    ) -> Saved:
        """Calculate and save an estimate.

        Calculate one product (estimate) or a declaration (entry) as POST /v1/estimates or POST
        /v1/estimates/entry would, and save it: only a saved estimate can be replayed, reported
        or notified in an incident. Needs the calculate permission; counted as the estimate is.
        Whichever is saved, an Idempotency-Key holds for one request of this route.

        Args:
            entry: A declaration to calculate and save, instead of estimate.
            estimate: One product to calculate and save. Give estimate or entry, not both.
            label: A name for the saved estimate.
            idempotency_key: Makes a retry of this call safe; a new one is generated for each
                call otherwise.
        """
        return self._request(
            "POST",
            "/v1/saved-estimates",
            model=Saved,
            body={"entry": entry, "estimate": estimate, "label": label},
            idempotent=True,
            idempotency_key=idempotency_key,
        )

    def get_saved_estimate(
        self,
        id: str,
    ) -> SavedDetail:
        """Read a saved estimate.

        One saved estimate: its request, as the engine read it, its result as it was calculated,
        never recalculated, and the incidents found since that concern it. Needs the read
        permission; not counted.

        Args:
            id: The id of the saved estimate, as its saving or the list gives it.
        """
        return self._request(
            "GET",
            f"/v1/saved-estimates/{quote(id, safe='')}",
            model=SavedDetail,
        )

    def get_status(
        self,
    ) -> Status:
        """Read the status and the coverage of the data.

        Freshness and verification of the data, the share of estimates withheld, the
        publications and the engine in service, and what is covered: Chapter 99 positions and
        their status, historical periods, base rates, agreements, fees, and what is out of
        scope. No key needed; the pages /status/ and /coverage/ read the same sources.
        """
        return self._request(
            "GET",
            "/v1/status",
            model=Status,
            auth=False,
        )


class AsyncOperations:
    """Each operation of the contract, under its operationId."""

    async def _request(
        self,
        method: str,
        path: str,
        *,
        model: type[_M],
        query: Mapping[str, Any] | None = None,
        body: Mapping[str, Any] | None = None,
        auth: bool = True,
        idempotent: bool = False,
        idempotency_key: str | None = None,
    ) -> _M:
        raise NotImplementedError

    async def list_agreements(
        self,
    ) -> AgreementList:
        """List the trade agreements.

        The agreements the engine applies, by the symbol of the HTS special column, with the
        origins each can apply to. A symbol does not establish eligibility: send it as
        preference, which declares the rules of origin met. Needs the read permission; not
        counted.
        """
        return await self._request(
            "GET",
            "/v1/agreements",
            model=AgreementList,
        )

    async def estimate(
        self,
        *,
        hts: str,
        origin: str,
        as_of: str | date | datetime | None = None,
        customs_value: int | float | Decimal | str | None = None,
        entry_type: Literal["formal", "informal"] | None = None,
        facts: Mapping[str, int | float | Decimal | str | bool] | None = None,
        freight: int | float | Decimal | str | None = None,
        include_fees: bool | None = None,
        insurance: int | float | Decimal | str | None = None,
        preference: str | None = None,
        publication_id: str | None = None,
        quantities: Mapping[str, int | float | Decimal | str] | None = None,
        transport_mode: Literal["air", "ocean", "land"] | None = None,
        idempotency_key: str | None = None,
    ) -> CalculationResult:
        """Estimate one product.

        Every US duty and fee that applies to one product at a date, each with its official
        source. Without a customs value, the duty rate. Not saved: an unsaved estimate cannot be
        replayed, reported or notified in an incident; save it with POST /v1/saved-estimates.
        Needs the calculate permission; counted in the quota unless it gives no figure of the
        duty: a question asked without any duty amount or rate (status needs_information), a
        code the tariff does not have or that names no product, a regime the service does not
        calculate. A question that gives the duty of each answer (scenarios), their bounds or
        the subtotal already known is counted.

        Args:
            hts: The HTS code of the goods: 4, 6, 8 or 10 digits, dots and spaces ignored. A
                rate needs the 10-digit statistical line or its 8-digit subheading.
            origin: Country of origin: where the goods were produced, not where they ship from.
                ISO 3166-1 alpha-2 (XK for Kosovo), or a code U.S. Customs files with (BU, GZ,
                KV, WE).
            as_of: When the goods are entered for consumption. A day, in New York time
                ("2026-04-05"); or, on a day when a measure takes effect at a stated hour, the
                instant of entry with its UTC offset ("2026-04-05T00:01:00-04:00"). Unset:
                today.
            customs_value: Customs value in US dollars: the transaction value declared, not a
                retail price. Unset: the duty rate is given, and an amount only where the duty
                does not depend on the value.
            entry_type: A formal entry pays the merchandise processing fee (MPF) on its value;
                an informal one, the fixed informal fee.
            facts: Answers to the questions of the facts catalogue (GET /v1/facts), by name. A
                name outside the catalogue is reported in the result and never used.
            freight: International freight in US dollars: no duty on it, it adds to the landed
                cost.
            include_fees: Count the entry fees (MPF, HMF) of a declaration of this product
                alone; the landed cost includes them only then. The MPF is charged once on a
                declaration: for several products entered together, use POST
                /v1/estimates/entry.
            insurance: Insurance of the shipment in US dollars: no duty on it, it adds to the
                landed cost.
            preference: A trade agreement's symbol from the HTS special column (S for USMCA, KR
                for KORUS…; GET /v1/agreements). Giving it declares that the goods meet its
                rules of origin and that you hold the proof.
            publication_id: Calculate with this publication of the rules rather than the one in
                force on the date: a saved result's publication_id replays it.
            quantities: Quantities in the units a duty counts (kg, l, item, dozen, pair,
                proof_liter…), nonnegative. A result names the quantity it needs in
                required_fields ("quantities.kg").
            transport_mode: How the goods arrive; by sea they also pay the harbor maintenance
                fee (HMF). Unset: land for goods of Canada or Mexico, ocean otherwise.
            idempotency_key: Makes a retry of this call safe; a new one is generated for each
                call otherwise.
        """
        return await self._request(
            "POST",
            "/v1/estimates",
            model=CalculationResult,
            body={"hts": hts, "origin": origin, "as_of": as_of, "customs_value": customs_value, "entry_type": entry_type, "facts": facts, "freight": freight, "include_fees": include_fees, "insurance": insurance, "preference": preference, "publication_id": publication_id, "quantities": quantities, "transport_mode": transport_mode},
            idempotent=True,
            idempotency_key=idempotency_key,
        )

    async def estimate_batch(
        self,
        *,
        items: Sequence[BatchItem],
        publication_id: str | None = None,
        idempotency_key: str | None = None,
    ) -> BatchResult:
        """Estimate up to 200 products.

        Each item calculated on its own, as POST /v1/estimates would, in the order given. An
        invalid item refuses the whole batch (422, error.fields naming items.<index>.<field>);
        an item that cannot be calculated (a date no edition covers) has its own error in
        results, the others are calculated. The batch's publication_id, if any, holds for every
        item. Counted as one request, whatever its number of items, unless none of them gives a
        figure of the duty (questions without any duty amount or rate, and errors, only). When
        the data is unavailable for every item, the batch is a 503 to send again, neither
        counted nor kept for its Idempotency-Key; when only for some, they have their error
        (data_unavailable) in results: send those items again.

        Args:
            items: The products, each calculated on its own.
            publication_id: Calculate with this publication of the rules rather than the one in
                force on the date: a saved result's publication_id replays it.
            idempotency_key: Makes a retry of this call safe; a new one is generated for each
                call otherwise.
        """
        return await self._request(
            "POST",
            "/v1/estimates/batch",
            model=BatchResult,
            body={"items": items, "publication_id": publication_id},
            idempotent=True,
            idempotency_key=idempotency_key,
        )

    async def estimate_entry(
        self,
        *,
        lines: Sequence[LineInput],
        as_of: str | date | datetime | None = None,
        entry_type: Literal["formal", "informal"] | None = None,
        facts: Mapping[str, int | float | Decimal | str | bool] | None = None,
        freight: int | float | Decimal | str | None = None,
        include_fees: bool | None = None,
        insurance: int | float | Decimal | str | None = None,
        publication_id: str | None = None,
        reference: str | None = None,
        transport_mode: Literal["air", "ocean", "land"] | None = None,
        idempotency_key: str | None = None,
    ) -> EntryResult:
        """Estimate a whole import declaration.

        Every line, then the MPF and the HMF once on the declaration: adding the estimates of
        the lines of one declaration gives a wrong MPF. Not saved: save it with POST /v1/saved-
        estimates (entry) to replay or report it. Counted as one request, whatever its number of
        lines, unless it gives no figure of the duty (a question without any duty amount or
        rate).

        Args:
            lines: The lines of the declaration, each a product.
            as_of: When the goods are entered for consumption. A day, in New York time
                ("2026-04-05"); or, on a day when a measure takes effect at a stated hour, the
                instant of entry with its UTC offset ("2026-04-05T00:01:00-04:00"). Unset:
                today.
            entry_type: A formal entry pays the merchandise processing fee (MPF) on its value;
                an informal one, the fixed informal fee.
            facts: Answers that hold for the whole declaration (GET /v1/facts, scope entry or
                shipment).
            freight: International freight in US dollars: no duty on it, it adds to the landed
                cost.
            include_fees: Count the entry fees (MPF, HMF) of the declaration.
            insurance: Insurance of the shipment in US dollars: no duty on it, it adds to the
                landed cost.
            publication_id: Calculate with this publication of the rules rather than the one in
                force on the date: a saved result's publication_id replays it.
            reference: Your reference for the declaration.
            transport_mode: How the goods arrive; by sea they also pay the harbor maintenance
                fee (HMF). Unset: land for goods of Canada or Mexico, ocean otherwise.
            idempotency_key: Makes a retry of this call safe; a new one is generated for each
                call otherwise.
        """
        return await self._request(
            "POST",
            "/v1/estimates/entry",
            model=EntryResult,
            body={"lines": lines, "as_of": as_of, "entry_type": entry_type, "facts": facts, "freight": freight, "include_fees": include_fees, "insurance": insurance, "publication_id": publication_id, "reference": reference, "transport_mode": transport_mode},
            idempotent=True,
            idempotency_key=idempotency_key,
        )

    async def estimate_history(
        self,
        *,
        hts: str,
        origin: str,
        customs_value: int | float | Decimal | str | None = None,
        entry_type: Literal["formal", "informal"] | None = None,
        facts: Mapping[str, int | float | Decimal | str | bool] | None = None,
        freight: int | float | Decimal | str | None = None,
        from_: str | date | None = None,
        include_fees: bool | None = None,
        insurance: int | float | Decimal | str | None = None,
        preference: str | None = None,
        quantities: Mapping[str, int | float | Decimal | str] | None = None,
        through: str | date | None = None,
        transport_mode: Literal["air", "ocean", "land"] | None = None,
        idempotency_key: str | None = None,
    ) -> HistoryResult:
        """Estimate one product at every change of the tariff.

        The product calculated on each first day of an edition, on each day a measure or a fee
        that covers it begins or ends, and on each day an incident or a notice not yet read
        begins or stops withholding its estimate, over the period asked, with the rules approved
        today. Counted as one request, whatever its number of points, unless no point gives a
        figure of the duty (a question without any duty amount or rate).

        Args:
            hts: The HTS code of the goods: 4, 6, 8 or 10 digits, dots and spaces ignored. A
                rate needs the 10-digit statistical line or its 8-digit subheading.
            origin: Country of origin: where the goods were produced, not where they ship from.
                ISO 3166-1 alpha-2 (XK for Kosovo), or a code U.S. Customs files with (BU, GZ,
                KV, WE).
            customs_value: Customs value in US dollars: the transaction value declared, not a
                retail price. Unset: the duty rate is given, and an amount only where the duty
                does not depend on the value.
            entry_type: A formal entry pays the merchandise processing fee (MPF) on its value;
                an informal one, the fixed informal fee.
            facts: Answers to the questions of the facts catalogue (GET /v1/facts), by name. A
                name outside the catalogue is reported in the result and never used.
            freight: International freight in US dollars: no duty on it, it adds to the landed
                cost.
            from_: First day of the period. Unset: the first edition the service holds.
            include_fees: Count the entry fees (MPF, HMF) of a declaration of this product
                alone; the landed cost includes them only then. The MPF is charged once on a
                declaration: for several products entered together, use POST
                /v1/estimates/entry.
            insurance: Insurance of the shipment in US dollars: no duty on it, it adds to the
                landed cost.
            preference: A trade agreement's symbol from the HTS special column (S for USMCA, KR
                for KORUS…; GET /v1/agreements). Giving it declares that the goods meet its
                rules of origin and that you hold the proof.
            quantities: Quantities in the units a duty counts (kg, l, item, dozen, pair,
                proof_liter…), nonnegative. A result names the quantity it needs in
                required_fields ("quantities.kg").
            through: Last day of the period, at most today. Unset: today.
            transport_mode: How the goods arrive; by sea they also pay the harbor maintenance
                fee (HMF). Unset: land for goods of Canada or Mexico, ocean otherwise.
            idempotency_key: Makes a retry of this call safe; a new one is generated for each
                call otherwise.
        """
        return await self._request(
            "POST",
            "/v1/estimates/history",
            model=HistoryResult,
            body={"hts": hts, "origin": origin, "customs_value": customs_value, "entry_type": entry_type, "facts": facts, "freight": freight, "from": from_, "include_fees": include_fees, "insurance": insurance, "preference": preference, "quantities": quantities, "through": through, "transport_mode": transport_mode},
            idempotent=True,
            idempotency_key=idempotency_key,
        )

    async def list_facts(
        self,
    ) -> FactList:
        """List the questions an estimate may ask.

        The facts catalogue: each question a measure may depend on, by the name to answer it
        with in facts, its type, its choices and its ordinary case. A result lists the ones it
        needs in input_guidance, and those it assumed in assumptions. Needs the read permission;
        not counted.
        """
        return await self._request(
            "GET",
            "/v1/facts",
            model=FactList,
        )

    async def search_hts(
        self,
        *,
        q: str | None = None,
        chapter: str | None = None,
        offset: int | None = None,
        limit: int | None = None,
    ) -> HtsSearch:
        """Search the US tariff schedule.

        The lines of the edition in service whose code starts with q, or whose descriptions hold
        every word of q, in code order; chapter (two digits) narrows them. A match is no
        classification. Needs the read permission; not counted.

        Args:
            q: A code, or words of the descriptions: 200 characters at most.
            chapter: Two digits, as 61: the lines of that chapter only.
            offset: How many lines to skip, from 0 to 100000.
            limit: How many lines to return, from 1 to 100.
        """
        return await self._request(
            "GET",
            "/v1/hts",
            model=HtsSearch,
            query={"q": q, "chapter": chapter, "offset": offset, "limit": limit},
        )

    async def get_hts(
        self,
        code: str,
    ) -> HtsDetail:
        """Read one line of the US tariff schedule.

        One line of the edition in service: its descriptions, its rate columns and its units.
        Needs the read permission; not counted.

        Args:
            code: An HTS code of 4, 6, 8 or 10 digits, with or without its dots.
        """
        return await self._request(
            "GET",
            f"/v1/hts/{quote(code, safe='')}",
            model=HtsDetail,
        )

    async def list_saved_estimates(
        self,
        *,
        offset: int | None = None,
        limit: int | None = None,
    ) -> SavedList:
        """List the saved estimates.

        The workspace's saved estimates, the latest first, saved from the API, the MCP or the
        portal. Needs the read permission; not counted.

        Args:
            offset: How many saved estimates to skip.
            limit: How many saved estimates to return, from 1 to 100.
        """
        return await self._request(
            "GET",
            "/v1/saved-estimates",
            model=SavedList,
            query={"offset": offset, "limit": limit},
        )

    async def save_estimate(
        self,
        *,
        entry: EntryInput | None = None,
        estimate: EstimateInput | None = None,
        label: str | None = None,
        idempotency_key: str | None = None,
    ) -> Saved:
        """Calculate and save an estimate.

        Calculate one product (estimate) or a declaration (entry) as POST /v1/estimates or POST
        /v1/estimates/entry would, and save it: only a saved estimate can be replayed, reported
        or notified in an incident. Needs the calculate permission; counted as the estimate is.
        Whichever is saved, an Idempotency-Key holds for one request of this route.

        Args:
            entry: A declaration to calculate and save, instead of estimate.
            estimate: One product to calculate and save. Give estimate or entry, not both.
            label: A name for the saved estimate.
            idempotency_key: Makes a retry of this call safe; a new one is generated for each
                call otherwise.
        """
        return await self._request(
            "POST",
            "/v1/saved-estimates",
            model=Saved,
            body={"entry": entry, "estimate": estimate, "label": label},
            idempotent=True,
            idempotency_key=idempotency_key,
        )

    async def get_saved_estimate(
        self,
        id: str,
    ) -> SavedDetail:
        """Read a saved estimate.

        One saved estimate: its request, as the engine read it, its result as it was calculated,
        never recalculated, and the incidents found since that concern it. Needs the read
        permission; not counted.

        Args:
            id: The id of the saved estimate, as its saving or the list gives it.
        """
        return await self._request(
            "GET",
            f"/v1/saved-estimates/{quote(id, safe='')}",
            model=SavedDetail,
        )

    async def get_status(
        self,
    ) -> Status:
        """Read the status and the coverage of the data.

        Freshness and verification of the data, the share of estimates withheld, the
        publications and the engine in service, and what is covered: Chapter 99 positions and
        their status, historical periods, base rates, agreements, fees, and what is out of
        scope. No key needed; the pages /status/ and /coverage/ read the same sources.
        """
        return await self._request(
            "GET",
            "/v1/status",
            model=Status,
            auth=False,
        )
