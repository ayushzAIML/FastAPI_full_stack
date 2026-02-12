from pathlib import Path
import warnings
import pandas as pd
import joblib

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", message=".*InconsistentVersionWarning.*")

CAR_PRICE_API_DIR = Path(__file__).resolve().parent
MODEL_PATH = CAR_PRICE_API_DIR / "random_forest_model.pkl"
COLS_PATH = CAR_PRICE_API_DIR / "feature_columns.pkl"
# MODEL_PATH = "/media/ayushz/New Volume/fast_api/project/car_price_api/app/random_forest_model.pkl"
# COLS_PATH = "/media/ayushz/New Volume/fast_api/project/car_price_api/app/feature_columns.pkl"

_model = None
_feature_columns = None


def load_artifacts():
    global _model, _feature_columns
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    if _feature_columns is None:
        _feature_columns = joblib.load(COLS_PATH)


def preprocess(payload: dict) -> pd.DataFrame:
    """
    Converts raw input into the SAME one-hot encoded column structure used in training.
    """
    df = pd.DataFrame([payload])

    df.rename(columns={
        "owner": "Owner",
        "year": "Year",
        "Present_price": "Present_Price",
    }, inplace=True)

    categorical_cols = ["Fuel_Type", "Seller_Type", "Transmission", "Owner", "Car_Name"]
    df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

    # Align columns to training columns (all at once to avoid fragmentation)
    df_encoded = df_encoded.reindex(columns=_feature_columns, fill_value=0)

    return df_encoded


def predict_price(payload: dict) -> float:
    load_artifacts()
    X = preprocess(payload)
    pred = _model.predict(X)[0]
    return float(pred)
