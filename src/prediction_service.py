from pathlib import Path

import joblib
import shap

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
# INITIALIZE SHAP EXPLAINER
# ============================================================

logger.info(
    "Initializing SHAP Tree Explainer"
)


explainer = shap.TreeExplainer(
    model
)


logger.info(
    "SHAP Tree Explainer initialized successfully"
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
            ]

        )

    )


    features_df = (
        online_features.to_df()
    )


    # ========================================================
    # REMOVE FEAST ENTITY COLUMN
    # ========================================================

    X_latest = (

        features_df

        .drop(
            columns=["city"],
            errors="ignore"
        )

    )


    # ========================================================
    # ENSURE EXACT MODEL FEATURE ORDER
    # ========================================================

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


    # ========================================================
    # GET LATEST FEATURES
    # ========================================================

    X_latest = (
        get_latest_features()
    )


    # ========================================================
    # PREDICT AQI
    # ========================================================

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


# ============================================================
# GET SHAP EXPLANATION
# ============================================================

def get_shap_explanation():

    logger.info(
        "Generating SHAP explanation"
    )


    # ========================================================
    # GET LATEST FEATURES
    # ========================================================

    X_latest = (
        get_latest_features()
    )


    # ========================================================
    # CALCULATE SHAP VALUES
    # ========================================================

    shap_values = (
        explainer.shap_values(
            X_latest
        )
    )


    # ========================================================
    # GET SINGLE PREDICTION VALUES
    # ========================================================

    shap_values_single = (
        shap_values[0]
    )


    feature_values = (

        X_latest
        .iloc[0]

    )


    # ========================================================
    # CREATE FEATURE EXPLANATIONS
    # ========================================================

    explanations = []


    for feature, feature_value, shap_value in zip(

        feature_names,

        feature_values,

        shap_values_single

    ):

        impact = (

            "increases AQI"

            if shap_value > 0

            else "decreases AQI"

        )


        explanations.append(

            {

                "feature": str(
                    feature
                ),

                "feature_value": round(

                    float(
                        feature_value
                    ),

                    4

                ),

                "shap_value": round(

                    float(
                        shap_value
                    ),

                    4

                ),

                "impact": impact

            }

        )


    # ========================================================
    # SORT BY IMPORTANCE
    # ========================================================

    explanations = sorted(

        explanations,

        key=lambda x: abs(
            x["shap_value"]
        ),

        reverse=True

    )


    logger.info(
        "SHAP explanation generated successfully"
    )


    return explanations