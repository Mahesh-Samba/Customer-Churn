
import json
from pathlib import Path

from allpairspy import AllPairs


PARAMETERS = {
    "tenure": [1, 12, 36, 72],
    "gender": ["Female", "Male"],
    "SeniorCitizen": [0, 1],
    "Partner": ["No", "Yes"],
    "Dependents": ["No", "Yes"],
    "MultipleLines": ["No", "Yes"],
    "InternetService": ["DSL", "Fiber optic", "No"],
    "OnlineSecurity": [
        "No", "Yes", "No internet service"
    ],
    "OnlineBackup": [
        "No", "Yes", "No internet service"
    ],
    "DeviceProtection": [
        "No", "Yes", "No internet service"
    ],
    "TechSupport": [
        "No", "Yes", "No internet service"
    ],
    "StreamingTV": [
        "No", "Yes", "No internet service"
    ],
    "StreamingMovies": [
        "No", "Yes", "No internet service"
    ],
    "Contract": [
        "Month-to-month", "One year", "Two year"
    ],
    "PaperlessBilling": ["No", "Yes"],
    "PaymentMethod": [
        "Bank transfer (automatic)",
        "Credit card (automatic)",
        "Electronic check",
        "Mailed check"
    ],
    "MonthlyCharges": [25.0, 70.3, 110.0]
}


SERVICE_FIELDS = [
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies"
]


def valid_combination(row):
    customer = dict(zip(PARAMETERS.keys(), row))

    services = [
        customer[field] for field in SERVICE_FIELDS
    ]

    if customer["InternetService"] == "No":
        return all(
            value == "No internet service"
            for value in services
        )

    return all(
        value != "No internet service"
        for value in services
    )


def main():
    field_names = list(PARAMETERS.keys())
    test_cases = []

    combinations = AllPairs(
        PARAMETERS.values(),
        filter_func=valid_combination
    )

    for index, values in enumerate(combinations, start=1):
        customer = dict(zip(field_names, values))

        customer["TotalCharges"] = round(
            customer["tenure"]
            * customer["MonthlyCharges"],
            2
        )

        test_cases.append({
            "test_case_id": f"TC{index:03d}",
            "scenario": "Pairwise-generated customer profile",
            "input": customer
        })

    Path("test_cases_pairwise.json").write_text(
        json.dumps(test_cases, indent=2),
        encoding="utf-8"
    )

    print(
        f"Generated {len(test_cases)} test cases "
        "in test_cases_pairwise.json"
    )


if __name__ == "__main__":
    main()
