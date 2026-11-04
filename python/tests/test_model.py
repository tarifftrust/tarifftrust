"""An answer read as objects, whatever it leaves out or adds."""

import json
from pathlib import Path

import pytest

from tarifftrust import TariffTrust, types
from tarifftrust._model import Model

CONTRACT = json.loads((Path(__file__).resolve().parents[2] / "openapi.json").read_text())


def test_nested_objects_are_objects():
    result = types.Estimate(
        {
            "status": "calculated",
            "duties": [{"name": "Base duty", "amount": "1.00", "source": {"title": "HTS"}}],
            "data": {"stale": False},
        }
    )
    assert result.duties[0].amount == "1.00"
    assert isinstance(result.duties[0], types.Duty)
    assert result.duties[0].source.title == "HTS"
    assert result.data.stale is False


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
    product = {name: None for name in types.AuditedEstimate._required}
    entry = {name: None for name in types.AuditedDeclaration._required}
    assert isinstance(types.SavedDetail({"result": product}).result, types.AuditedEstimate)
    assert isinstance(types.SavedDetail({"result": entry}).result, types.AuditedDeclaration)


def test_a_field_left_out_reads_as_its_default_or_none():
    result = types.Estimate({"status": "calculated"})
    assert result.warnings is None and result.duties is None and result.saved_estimate_id is None


def test_null_stays_null():
    result = types.Estimate(
        {"estimated_duty": None, "estimated_duty_rate": None, "candidates": None}
    )
    assert result.estimated_duty is None
    assert result.estimated_duty_rate is None and result.candidates is None


def test_a_field_newer_than_the_package_reads_too():
    result = types.Estimate({"new_field": 1})
    assert result.new_field == 1 and "new_field" in dir(result)


def test_a_mistyped_field_is_an_error():
    with pytest.raises(AttributeError, match="no field 'estimated_dutty'"):
        _ = types.Estimate({}).estimated_dutty


def test_a_reserved_word_reads_with_an_underscore():
    assert types.CoveredWindow({"from": "2025-01-01"}).from_ == "2025-01-01"


def test_to_dict_is_what_the_api_sent():
    data = {"status": "calculated", "duties": [{"name": "Base duty"}]}
    result = types.Estimate(data)
    assert result.duties[0].name == "Base duty"
    assert result.to_dict() == data
    assert json.loads(json.dumps(result.to_dict())) == data


def test_comparison_and_repr():
    one = types.Source({"sha256": "abc", "title": "HTS", "nested": {"a": 1}})
    assert one == types.Source(one.to_dict()) and one != types.Duty(one.to_dict())
    assert repr(one) == "Source(sha256='abc', title='HTS')"


def test_an_object_can_be_copied():
    import copy
    import pickle

    one = types.Source({"title": "HTS"})
    assert copy.deepcopy(one) == one and pickle.loads(pickle.dumps(one)) == one


def test_every_object_of_the_contract_is_declared():
    inputs = {"BatchItem", "BatchRequest", "EntryRequest", "EstimateRequest", "HistoryRequest"}
    inputs |= {"LineInput"}
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
