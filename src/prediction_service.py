from pathlib import Path

import joblib
from feast import FeatureStore

from src.config import CITY

from app.logger import logger


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)


FEATURE_REPO_PATH = (
    PROJECT_ROOT
    / "feature_repo"
    / "feature_repo"
)


MODEL_PATH = (
    PROJECT_ROOT
    / "notebooks"
    / "models"
    / "karachi_aqi_random_forest.pkl"
)


FEATURE_NAMES_PATH = (
    PROJECT_ROOT
    / "notebooks"
    / "models"
    / "feature_names.pkl"
)


# ============================================================
# LOAD MODEL
# ============================================================

logger.info(
    "Loading Random Forest model"
)

model = joblib.load(
    MODEL_PATH
)

logger.info(
    "Random Forest model loaded successfully"
)


# ============================================================
# LOAD FEATURE NAMES
# ============================================================

feature_names = joblib.load(
    FEATURE_NAMES_PATH
)

logger.info(
    f"Loaded {len(feature_names)} feature names"
)


# ============================================================
# CONNECT TO FEAST
# ============================================================

store = FeatureStore(
    repo_path=str(
        FEATURE_REPO_PATH
    )
)

logger.info(
    "Connected to Feast Feature Store"
)


# ============================================================
# GET LATEST FEATURES FROM FEAST
# ============================================================

def get_latest_features():

    logger.info(
        "Retrieving latest features from Feast"
    )


    feast_features = [

        f"karachi_aqi_features:{feature}"

        for feature in feature_names

    ]


    online_features = (

        store.get_online_features(

            features=feast_features,

            entity_rows=[
                {
                    "city": CITY
                }
            ],

        )

    )


    features_df = (
        online_features.to_df()
    )


    # Remove Feast entity column

    X_latest = (

        features_df

        .drop(
            columns=["city"]
        )

    )


    # Ensure exact model feature order

    X_latest = (

        X_latest[
            feature_names
        ]

    )


    logger.info(

        f"Retrieved {len(feature_names)} "

        "features from Feast successfully"

    )


    return X_latest


# ============================================================
# MAKE AQI PREDICTION
# ============================================================

def predict_aqi():

    logger.info(
        "Starting AQI prediction"
    )


    # Get latest features
    # directly from Feast

    X_latest = (
        get_latest_features()
    )


    # Predict AQI

    prediction = (

        model.predict(
            X_latest
        )[0]

    )


    logger.info(

        f"AQI prediction completed: "

        f"{prediction}"

    )


    return float(
        prediction
    )