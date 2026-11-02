"""An answer read as objects, whatever it leaves out or adds."""

import json
from pathlib import Path

import pytest

from tarifftrust import TariffTrust, types
from tarifftrust._model import Model

CONTRACT = json.loads((Path(__file__).resolve().parents[2] / "openapi.json").read_text())


def test_nested_objects_are_objects():
    result = types.CalculationResult(
        {
            "status": "calculated",
            "components": [{"id": "base", "amount": "1.00", "source": {"authority": "USITC"}}],
            "freshness": {"stale": False},
        }
    )
    assert result.components[0].amount == "1.00"
    assert isinstance(result.components[0], types.Component)
    assert result.components[0].source.authority == "USITC"
    assert result.freshness.stale is False


def test_a_map_of_objects_is_a_map_of_objects():
    batch = types.BatchResult({"freshness": {"pub": {"stale": True}}})
    assert batch.freshness["pub"].stale is True


def test_a_union_is_the_object_whose_required_fields_are_there():
    batch = types.BatchResult(
        {
            "results": [
                {"index": 0, "result": {"status": "calculated"}},
                {"index": 1, "error": {"code": "invalid_input"}},
            ]
        }
    )
    success, failure = batch.results
    assert isinstance(success, types.BatchSuccess) and success.result.status == "calculated"
    assert isinstance(failure, types.BatchFailure) and failure.error.code == "invalid_input"


def test_a_saved_estimate_is_a_product_or_a_declaration():
    product = {name: None for name in types.CalculationResult._required}
    entry = {name: None for name in types.EntryResult._required}
    assert isinstance(types.Saved({"result": product}).result, types.CalculationResult)
    assert isinstance(types.Saved({"result": entry}).result, types.EntryResult)


def test_a_field_left_out_reads_as_its_default_or_none():
    result = types.CalculationResult({"status": "calculated"})
    assert result.review_pending == [] and result.assumptions == []
    assert result.verification is None and result.duty_rate is None
    result.review_pending.append("mine")
    assert types.CalculationResult({}).review_pending == []


def test_null_stays_null():
    result = types.CalculationResult(
        {"estimated_duty": None, "duty_rate": None, "candidates": None}
    )
    assert result.estimated_duty is None and result.duty_rate is None and result.candidates is None


def test_a_field_newer_than_the_package_reads_too():
    result = types.CalculationResult({"new_field": 1})
    assert result.new_field == 1 and "new_field" in dir(result)


def test_a_mistyped_field_is_an_error():
    with pytest.raises(AttributeError, match="no field 'estimated_dutty'"):
        _ = types.CalculationResult({}).estimated_dutty


def test_a_reserved_word_reads_with_an_underscore():
    assert types.CoveredWindow({"from": "2025-01-01"}).from_ == "2025-01-01"


def test_to_dict_is_what_the_api_sent():
    data = {"status": "calculated", "components": [{"id": "base"}]}
    result = types.CalculationResult(data)
    assert result.components[0].id == "base"
    assert result.to_dict() == data
    assert json.loads(json.dumps(result.to_dict())) == data


def test_comparison_and_repr():
    one = types.Source({"authority": "USITC", "title": "HTS", "nested": {"a": 1}})
    assert one == types.Source(one.to_dict()) and one != types.Fee(one.to_dict())
    assert repr(one) == "Source(authority='USITC', title='HTS')"


def test_an_object_can_be_copied():
    import copy
    import pickle

    one = types.Source({"authority": "USITC"})
    assert copy.deepcopy(one) == one and pickle.loads(pickle.dumps(one)) == one


def test_every_object_of_the_contract_is_declared():
    inputs = {"BatchItem", "BatchRequest", "EntryInput", "EstimateInput", "HistoryRequest"}
    inputs |= {"LineInput", "SaveRequest"}
    for name, schema in CONTRACT["components"]["schemas"].items():
        if name in inputs:
            continue
        kind = getattr(types, name)
        assert issubclass(kind, Model)
        assert kind._fields == set(schema["properties"]), name
        assert kind._required == set(schema.get("required", [])), name
        for field in schema["properties"]:
            assert field in dir(kind({})), (name, field)


def test_every_operation_of_the_contract_is_a_method():
    for item in CONTRACT["paths"].values():
        for operation in item.values():
            assert callable(getattr(TariffTrust, operation["operationId"]))
