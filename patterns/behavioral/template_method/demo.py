import json

from patterns.behavioral.template_method.pattern import ApiPipeline, CsvPipeline

CSV_DATA = "name,amount\nalice,10\nbob,\ncarol,30\n"
API_DATA = json.dumps({"results": [
    {"name": "dave smith", "amount": 5},
    {"name": "erin jones", "amount": None},
    {"name": "frank lee", "amount": 7},
]})


def run() -> None:
    print("=== Template Method: ETL Data Pipeline ===")
    for label, pipeline in (("CSV", CsvPipeline(CSV_DATA)), ("API", ApiPipeline(API_DATA))):
        print(f"\n[{label}] running pipeline")
        for line in pipeline.run():
            print(f"  - {line}")
        print(f"  warehouse: {pipeline.warehouse}")


if __name__ == "__main__":
    run()
