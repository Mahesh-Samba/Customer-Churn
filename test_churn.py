
import json
import math
from pathlib import Path

import pytest

from churn_prediction import predict_churn


BASE_DIR = Path(__file__).resolve().parent
APP_DIR = Path(__file__).resolve().parent

CASES_PATH = BASE_DIR / "test_cases.json"
RESULTS_PATH = BASE_DIR / "prediction_results.json"


# Utility functions
APP_DIR = Path(__file__).resolve().parent

CASES = json.loads(
    CASES_PATH.read_text(encoding="utf-8")
)


@pytest.mark.parametrize(
    "case",
    CASES,
    ids=lambda case: case["test_case_id"]
)
def test_churn_prediction(case):

    # Input payload from JSON
    customer_input = case["input"]

    # Call the prediction function
    result = predict_churn(customer_input)

    # Validate prediction label
    assert result["Prediction"] in {"Yes", "No"}

    # Validate churn probability
    probability = result["Churn probability"]

    assert isinstance(probability, (int, float))
    assert math.isfinite(probability)
    assert 0.0 <= probability <= 1.0

    # Read existing results, if available
    if RESULTS_PATH.exists():
        try:
            results = json.loads(
                RESULTS_PATH.read_text(encoding="utf-8")
            )
        except json.JSONDecodeError:
            results = []
    else:
        results = []

    # Avoid duplicate entries when rerunning a test
    results = [
        item for item in results
        if item.get("test_case_id") != case["test_case_id"]
    ]

    # Save actual response
    results.append({
        "test_case_id": case["test_case_id"],
        "scenario": case.get("scenario"),
        "input": customer_input,
        "output": result,
        "status": "PASS"
    })

    RESULTS_PATH.write_text(
        json.dumps(results, indent=2),
        encoding="utf-8"
    )
