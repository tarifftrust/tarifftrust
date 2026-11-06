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
    Declaration,
    Estimate,
    FactList,
    HistoryResult,
    HtsDetail,
    HtsSearch,
    LineInput,
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
            "/v2/agreements",
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
        label: str | None = None,
        preference: str | None = None,
        publication_id: str | None = None,
        quantities: Mapping[str, int | float | Decimal | str] | None = None,
        save: bool | None = None,
        transport_mode: Literal["air", "ocean", "land"] | None = None,
        idempotency_key: str | None = None,
    ) -> Estimate:
        """Estimate one product.

        Every US duty and fee that applies to one product at a date, each with its official
        source. Without a customs value, the duty rate when the duties are percentages. When
        something is missing to give a figure, the answer says what to send again. Send save to
        keep the estimate. Needs the calculate permission; counted in the quota unless it gives
        no figure of the duty: status needs_information, not_found, not_covered or unsupported.

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
            entry_type: A formal entry pays the merchandise processing fee (MPF) on its value.
                An informal entry pays a fixed fee the estimate does not calculate: it gives no
                fees.
            facts: Answers to the questions of the facts catalogue (GET /v2/facts), by name. A
                name that is no question is refused, so that a typing error never gives a figure
                on the ordinary case.
            freight: International freight in US dollars: no duty on it, it adds to the landed
                cost.
            include_fees: Count the entry fees (MPF, HMF) of a declaration of this product
                alone. Each product is estimated as its own declaration: the MPF is charged once
                on a declaration, so for several products entered together use POST
                /v2/estimates/entry.
            insurance: Insurance of the shipment in US dollars: no duty on it, it adds to the
                landed cost.
            label: A name for the saved estimate; needs save.
            preference: A trade agreement's symbol from the HTS special column (S for USMCA, KR
                for KORUS…; GET /v2/agreements). Giving it declares that the goods meet its
                rules of origin and that you hold the proof.
            publication_id: Calculate with this publication of the rules instead of the one in
                service on that date: the data.publication_id of an earlier answer gives the
                same result again, as long as the engine has not changed.
            quantities: Quantities in the units a duty counts (kg, l, item, dozen, pair,
                proof_liter…), nonnegative. An answer names the quantity it needs in missing
                ("quantities.kg").
            save: Save the estimate: only a saved estimate keeps its detail, is reported, and is
                notified if a rate proves wrong. An answer without a figure is not saved. Send
                an Idempotency-Key: without one, a request sent again after a timeout saves
                twice.
            transport_mode: How the goods arrive; by sea they also pay the harbor maintenance
                fee (HMF). Unset: land for goods of Canada or Mexico, ocean otherwise.
            idempotency_key: Makes a retry of this call safe; a new one is generated for each
                call otherwise.
        """
        return self._request(
            "POST",
            "/v2/estimates",
            model=Estimate,
            body={"hts": hts, "origin": origin, "as_of": as_of, "customs_value": customs_value, "entry_type": entry_type, "facts": facts, "freight": freight, "include_fees": include_fees, "insurance": insurance, "label": label, "preference": preference, "publication_id": publication_id, "quantities": quantities, "save": save, "transport_mode": transport_mode},
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

        Each item calculated on its own, as POST /v2/estimates would, in the order given: each
        is its own declaration, so do not add their fees up; for several products entered
        together, use POST /v2/estimates/entry. An invalid item refuses the whole batch (422,
        error.fields naming items.<index>.<field>); an item that cannot be calculated (a date no
        edition covers) has its own error in results, the others are calculated. The batch's
        publication_id, if any, holds for every item. Counted as one request, whatever its
        number of items, unless none of them gives a figure of the duty. When the data is
        unavailable for every item, the batch is a 503 to send again, neither counted nor kept
        for its Idempotency-Key; when only for some, they have their error (data_unavailable) in
        results: send those items again.

        Args:
            items: The products, each calculated on its own.
            publication_id: Calculate with this publication of the rules instead of the one in
                service on that date: the data.publication_id of an earlier answer gives the
                same result again, as long as the engine has not changed.
            idempotency_key: Makes a retry of this call safe; a new one is generated for each
                call otherwise.
        """
        return self._request(
            "POST",
            "/v2/estimates/batch",
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
        label: str | None = None,
        publication_id: str | None = None,
        reference: str | None = None,
        save: bool | None = None,
        transport_mode: Literal["air", "ocean", "land"] | None = None,
        idempotency_key: str | None = None,
    ) -> Declaration:
        """Estimate a whole import declaration.

        Every line, then the MPF and the HMF once on the declaration: adding the estimates of
        the lines of one declaration gives a wrong MPF. Send save to keep the estimate. Counted
        as one request, whatever its number of lines, unless it gives no figure of the duty.

        Args:
            lines: The lines of the declaration, each a product.
            as_of: When the goods are entered for consumption. A day, in New York time
                ("2026-04-05"); or, on a day when a measure takes effect at a stated hour, the
                instant of entry with its UTC offset ("2026-04-05T00:01:00-04:00"). Unset:
                today.
            entry_type: A formal entry pays the merchandise processing fee (MPF) on its value.
                An informal entry pays a fixed fee the estimate does not calculate: it gives no
                fees.
            facts: Answers that hold for the whole declaration (GET /v2/facts, scope entry or
                shipment).
            freight: International freight in US dollars: no duty on it, it adds to the landed
                cost.
            include_fees: Count the entry fees (MPF, HMF) of the declaration.
            insurance: Insurance of the shipment in US dollars: no duty on it, it adds to the
                landed cost.
            label: A name for the saved estimate; needs save.
            publication_id: Calculate with this publication of the rules instead of the one in
                service on that date: the data.publication_id of an earlier answer gives the
                same result again, as long as the engine has not changed.
            reference: Your reference for the declaration.
            save: Save the estimate: only a saved estimate keeps its detail, is reported, and is
                notified if a rate proves wrong. An answer without a figure is not saved. Send
                an Idempotency-Key: without one, a request sent again after a timeout saves
                twice.
            transport_mode: How the goods arrive; by sea they also pay the harbor maintenance
                fee (HMF). Unset: land for goods of Canada or Mexico, ocean otherwise.
            idempotency_key: Makes a retry of this call safe; a new one is generated for each
                call otherwise.
        """
        return self._request(
            "POST",
            "/v2/estimates/entry",
            model=Declaration,
            body={"lines": lines, "as_of": as_of, "entry_type": entry_type, "facts": facts, "freight": freight, "include_fees": include_fees, "insurance": insurance, "label": label, "publication_id": publication_id, "reference": reference, "save": save, "transport_mode": transport_mode},
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
        figure of the duty.

        Args:
            hts: The HTS code of the goods: 4, 6, 8 or 10 digits, dots and spaces ignored. A
                rate needs the 10-digit statistical line or its 8-digit subheading.
            origin: Country of origin: where the goods were produced, not where they ship from.
                ISO 3166-1 alpha-2 (XK for Kosovo), or a code U.S. Customs files with (BU, GZ,
                KV, WE).
            customs_value: Customs value in US dollars: the transaction value declared, not a
                retail price. Unset: the duty rate is given, and an amount only where the duty
                does not depend on the value.
            entry_type: A formal entry pays the merchandise processing fee (MPF) on its value.
                An informal entry pays a fixed fee the estimate does not calculate: it gives no
                fees.
            facts: Answers to the questions of the facts catalogue (GET /v2/facts), by name. A
                name that is no question is refused, so that a typing error never gives a figure
                on the ordinary case.
            freight: International freight in US dollars: no duty on it, it adds to the landed
                cost.
            from_: First day of the period. Unset: the first edition the service holds.
            include_fees: Count the entry fees (MPF, HMF) of a declaration of this product
                alone. Each product is estimated as its own declaration: the MPF is charged once
                on a declaration, so for several products entered together use POST
                /v2/estimates/entry.
            insurance: Insurance of the shipment in US dollars: no duty on it, it adds to the
                landed cost.
            preference: A trade agreement's symbol from the HTS special column (S for USMCA, KR
                for KORUS…; GET /v2/agreements). Giving it declares that the goods meet its
                rules of origin and that you hold the proof.
            quantities: Quantities in the units a duty counts (kg, l, item, dozen, pair,
                proof_liter…), nonnegative. An answer names the quantity it needs in missing
                ("quantities.kg").
            through: Last day of the period, at most today. Unset: today.
            transport_mode: How the goods arrive; by sea they also pay the harbor maintenance
                fee (HMF). Unset: land for goods of Canada or Mexico, ocean otherwise.
            idempotency_key: Makes a retry of this call safe; a new one is generated for each
                call otherwise.
        """
        return self._request(
            "POST",
            "/v2/estimates/history",
            model=HistoryResult,
            body={"hts": hts, "origin": origin, "customs_value": customs_value, "entry_type": entry_type, "facts": facts, "freight": freight, "from": from_, "include_fees": include_fees, "insurance": insurance, "preference": preference, "quantities": quantities, "through": through, "transport_mode": transport_mode},
            idempotent=True,
            idempotency_key=idempotency_key,
        )

    def list_facts(
        self,
    ) -> FactList:
        """List the questions an estimate may ask.

        The questions that can change an answer today: each by the name to answer it with in
        facts, its type, its choices and its ordinary case. An answer names the ones it needs in
        missing, and those it rests on in facts. The example shows two of them; the answer lists
        them all. Needs the read permission; not counted.
        """
        return self._request(
            "GET",
            "/v2/facts",
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
            "/v2/hts",
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
            f"/v2/hts/{quote(code, safe='')}",
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
            "/v2/saved-estimates",
            model=SavedList,
            query={"offset": offset, "limit": limit},
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
            f"/v2/saved-estimates/{quote(id, safe='')}",
            model=SavedDetail,
        )

    def get_status(
        self,
    ) -> Status:
        """Read the status of the data.

        Whether the data can be relied on now, which publication and engine answer, when the
        official sources were last checked, the first day covered and the wrong rates being
        corrected. No key needed; the pages /status/ and /coverage/ say more.
        """
        return self._request(
            "GET",
            "/v2/status",
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
            "/v2/agreements",
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
        label: str | None = None,
        preference: str | None = None,
        publication_id: str | None = None,
        quantities: Mapping[str, int | float | Decimal | str] | None = None,
        save: bool | None = None,
        transport_mode: Literal["air", "ocean", "land"] | None = None,
        idempotency_key: str | None = None,
    ) -> Estimate:
        """Estimate one product.

        Every US duty and fee that applies to one product at a date, each with its official
        source. Without a customs value, the duty rate when the duties are percentages. When
        something is missing to give a figure, the answer says what to send again. Send save to
        keep the estimate. Needs the calculate permission; counted in the quota unless it gives
        no figure of the duty: status needs_information, not_found, not_covered or unsupported.

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
            entry_type: A formal entry pays the merchandise processing fee (MPF) on its value.
                An informal entry pays a fixed fee the estimate does not calculate: it gives no
                fees.
            facts: Answers to the questions of the facts catalogue (GET /v2/facts), by name. A
                name that is no question is refused, so that a typing error never gives a figure
                on the ordinary case.
            freight: International freight in US dollars: no duty on it, it adds to the landed
                cost.
            include_fees: Count the entry fees (MPF, HMF) of a declaration of this product
                alone. Each product is estimated as its own declaration: the MPF is charged once
                on a declaration, so for several products entered together use POST
                /v2/estimates/entry.
            insurance: Insurance of the shipment in US dollars: no duty on it, it adds to the
                landed cost.
            label: A name for the saved estimate; needs save.
            preference: A trade agreement's symbol from the HTS special column (S for USMCA, KR
                for KORUS…; GET /v2/agreements). Giving it declares that the goods meet its
                rules of origin and that you hold the proof.
            publication_id: Calculate with this publication of the rules instead of the one in
                service on that date: the data.publication_id of an earlier answer gives the
                same result again, as long as the engine has not changed.
            quantities: Quantities in the units a duty counts (kg, l, item, dozen, pair,
                proof_liter…), nonnegative. An answer names the quantity it needs in missing
                ("quantities.kg").
            save: Save the estimate: only a saved estimate keeps its detail, is reported, and is
                notified if a rate proves wrong. An answer without a figure is not saved. Send
                an Idempotency-Key: without one, a request sent again after a timeout saves
                twice.
            transport_mode: How the goods arrive; by sea they also pay the harbor maintenance
                fee (HMF). Unset: land for goods of Canada or Mexico, ocean otherwise.
            idempotency_key: Makes a retry of this call safe; a new one is generated for each
                call otherwise.
        """
        return await self._request(
            "POST",
            "/v2/estimates",
            model=Estimate,
            body={"hts": hts, "origin": origin, "as_of": as_of, "customs_value": customs_value, "entry_type": entry_type, "facts": facts, "freight": freight, "include_fees": include_fees, "insurance": insurance, "label": label, "preference": preference, "publication_id": publication_id, "quantities": quantities, "save": save, "transport_mode": transport_mode},
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

        Each item calculated on its own, as POST /v2/estimates would, in the order given: each
        is its own declaration, so do not add their fees up; for several products entered
        together, use POST /v2/estimates/entry. An invalid item refuses the whole batch (422,
        error.fields naming items.<index>.<field>); an item that cannot be calculated (a date no
        edition covers) has its own error in results, the others are calculated. The batch's
        publication_id, if any, holds for every item. Counted as one request, whatever its
        number of items, unless none of them gives a figure of the duty. When the data is
        unavailable for every item, the batch is a 503 to send again, neither counted nor kept
        for its Idempotency-Key; when only for some, they have their error (data_unavailable) in
        results: send those items again.

        Args:
            items: The products, each calculated on its own.
            publication_id: Calculate with this publication of the rules instead of the one in
                service on that date: the data.publication_id of an earlier answer gives the
                same result again, as long as the engine has not changed.
            idempotency_key: Makes a retry of this call safe; a new one is generated for each
                call otherwise.
        """
        return await self._request(
            "POST",
            "/v2/estimates/batch",
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
        label: str | None = None,
        publication_id: str | None = None,
        reference: str | None = None,
        save: bool | None = None,
        transport_mode: Literal["air", "ocean", "land"] | None = None,
        idempotency_key: str | None = None,
    ) -> Declaration:
        """Estimate a whole import declaration.

        Every line, then the MPF and the HMF once on the declaration: adding the estimates of
        the lines of one declaration gives a wrong MPF. Send save to keep the estimate. Counted
        as one request, whatever its number of lines, unless it gives no figure of the duty.

        Args:
            lines: The lines of the declaration, each a product.
            as_of: When the goods are entered for consumption. A day, in New York time
                ("2026-04-05"); or, on a day when a measure takes effect at a stated hour, the
                instant of entry with its UTC offset ("2026-04-05T00:01:00-04:00"). Unset:
                today.
            entry_type: A formal entry pays the merchandise processing fee (MPF) on its value.
                An informal entry pays a fixed fee the estimate does not calculate: it gives no
                fees.
            facts: Answers that hold for the whole declaration (GET /v2/facts, scope entry or
                shipment).
            freight: International freight in US dollars: no duty on it, it adds to the landed
                cost.
            include_fees: Count the entry fees (MPF, HMF) of the declaration.
            insurance: Insurance of the shipment in US dollars: no duty on it, it adds to the
                landed cost.
            label: A name for the saved estimate; needs save.
            publication_id: Calculate with this publication of the rules instead of the one in
                service on that date: the data.publication_id of an earlier answer gives the
                same result again, as long as the engine has not changed.
            reference: Your reference for the declaration.
            save: Save the estimate: only a saved estimate keeps its detail, is reported, and is
                notified if a rate proves wrong. An answer without a figure is not saved. Send
                an Idempotency-Key: without one, a request sent again after a timeout saves
                twice.
            transport_mode: How the goods arrive; by sea they also pay the harbor maintenance
                fee (HMF). Unset: land for goods of Canada or Mexico, ocean otherwise.
            idempotency_key: Makes a retry of this call safe; a new one is generated for each
                call otherwise.
        """
        return await self._request(
            "POST",
            "/v2/estimates/entry",
            model=Declaration,
            body={"lines": lines, "as_of": as_of, "entry_type": entry_type, "facts": facts, "freight": freight, "include_fees": include_fees, "insurance": insurance, "label": label, "publication_id": publication_id, "reference": reference, "save": save, "transport_mode": transport_mode},
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
        figure of the duty.

        Args:
            hts: The HTS code of the goods: 4, 6, 8 or 10 digits, dots and spaces ignored. A
                rate needs the 10-digit statistical line or its 8-digit subheading.
            origin: Country of origin: where the goods were produced, not where they ship from.
                ISO 3166-1 alpha-2 (XK for Kosovo), or a code U.S. Customs files with (BU, GZ,
                KV, WE).
            customs_value: Customs value in US dollars: the transaction value declared, not a
                retail price. Unset: the duty rate is given, and an amount only where the duty
                does not depend on the value.
            entry_type: A formal entry pays the merchandise processing fee (MPF) on its value.
                An informal entry pays a fixed fee the estimate does not calculate: it gives no
                fees.
            facts: Answers to the questions of the facts catalogue (GET /v2/facts), by name. A
                name that is no question is refused, so that a typing error never gives a figure
                on the ordinary case.
            freight: International freight in US dollars: no duty on it, it adds to the landed
                cost.
            from_: First day of the period. Unset: the first edition the service holds.
            include_fees: Count the entry fees (MPF, HMF) of a declaration of this product
                alone. Each product is estimated as its own declaration: the MPF is charged once
                on a declaration, so for several products entered together use POST
                /v2/estimates/entry.
            insurance: Insurance of the shipment in US dollars: no duty on it, it adds to the
                landed cost.
            preference: A trade agreement's symbol from the HTS special column (S for USMCA, KR
                for KORUS…; GET /v2/agreements). Giving it declares that the goods meet its
                rules of origin and that you hold the proof.
            quantities: Quantities in the units a duty counts (kg, l, item, dozen, pair,
                proof_liter…), nonnegative. An answer names the quantity it needs in missing
                ("quantities.kg").
            through: Last day of the period, at most today. Unset: today.
            transport_mode: How the goods arrive; by sea they also pay the harbor maintenance
                fee (HMF). Unset: land for goods of Canada or Mexico, ocean otherwise.
            idempotency_key: Makes a retry of this call safe; a new one is generated for each
                call otherwise.
        """
        return await self._request(
            "POST",
            "/v2/estimates/history",
            model=HistoryResult,
            body={"hts": hts, "origin": origin, "customs_value": customs_value, "entry_type": entry_type, "facts": facts, "freight": freight, "from": from_, "include_fees": include_fees, "insurance": insurance, "preference": preference, "quantities": quantities, "through": through, "transport_mode": transport_mode},
            idempotent=True,
            idempotency_key=idempotency_key,
        )

    async def list_facts(
        self,
    ) -> FactList:
        """List the questions an estimate may ask.

        The questions that can change an answer today: each by the name to answer it with in
        facts, its type, its choices and its ordinary case. An answer names the ones it needs in
        missing, and those it rests on in facts. The example shows two of them; the answer lists
        them all. Needs the read permission; not counted.
        """
        return await self._request(
            "GET",
            "/v2/facts",
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
            "/v2/hts",
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
            f"/v2/hts/{quote(code, safe='')}",
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
            "/v2/saved-estimates",
            model=SavedList,
            query={"offset": offset, "limit": limit},
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
            f"/v2/saved-estimates/{quote(id, safe='')}",
            model=SavedDetail,
        )

    async def get_status(
        self,
    ) -> Status:
        """Read the status of the data.

        Whether the data can be relied on now, which publication and engine answer, when the
        official sources were last checked, the first day covered and the wrong rates being
        corrected. No key needed; the pages /status/ and /coverage/ say more.
        """
        return await self._request(
            "GET",
            "/v2/status",
            model=Status,
            auth=False,
        )
