
import os
import streamlit_app as app

from pathlib import Path

APP_DIR = Path(__file__).resolve().parent

DEFAULT_DATA_PATH = APP_DIR / "Customer-Churn (1).csv"


# DEFAULT_MODEL_PATH = r"F:\KN Academy - Projects\Machine Learning\Telecom Customer Churn\best_xgboost_churn_model.pkl"


def predict_churn(user_input, data_path=None, model_path=None):
    data_path = (
        data_path
        or os.getenv("CHURN_DATA_PATH")
        or DEFAULT_DATA_PATH
    )

    model_path = (
        model_path
        or os.getenv(path='best_xgboost_churn_model.pkl')
    )

    # Reuse your existing application functions
    df = app.load_data(data_path)
    prep = app.build_preprocessor(df)
    model = app.load_model(model_path)

    # Apply the existing preprocessing
    X = app.preprocess_input(user_input, prep)

    # Generate prediction
    predicted_class = int(model.predict(X)[0])

    churn_probability = float(
        model.predict_proba(X)[0][1]
    )

    return {
        "Prediction": (
            "Yes" if predicted_class == 1 else "No"
        ),
        "Churn probability": churn_probability,
        "predicted_class": predicted_class
    }
