import json

from patterns.behavioral.template_method.pattern import ApiPipeline, CsvPipeline


def test_csv_pipeline_steps_in_order_and_filters():
    p = CsvPipeline("name,amount\na,1\nb,\n")
    log = p.run()
    assert log == ["extracted 2 records", "transformed to 1 records"]
    assert p.warehouse == [{"name": "a", "amount": "1"}]


def test_api_pipeline_overrides_transform_and_hook():
    payload = json.dumps({"results": [{"name": "x y", "v": 1}, {"name": "z", "v": None}]})
    p = ApiPipeline(payload)
    log = p.run()
    assert p.warehouse == [{"name": "X Y", "v": 1}]
    assert log[-1] == "notification sent"
