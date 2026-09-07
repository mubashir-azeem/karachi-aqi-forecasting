from pathlib import Path

import joblib
import pandas as pd
from feast import FeatureStore


# =========================================================
# PROJECT PATHS
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

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


# =========================================================
# LOAD TRAINED MODEL
# =========================================================

model = joblib.load(MODEL_PATH)

print("\nModel loaded successfully!")


# =========================================================
# LOAD EXACT FEATURE ORDER
# =========================================================

feature_names = joblib.load(FEATURE_NAMES_PATH)

print("Number of features expected by model:", len(feature_names))


# =========================================================
# CONNECT TO FEAST
# =========================================================

store = FeatureStore(
    repo_path=str(FEATURE_REPO_PATH)
)


# =========================================================
# CREATE FEAST FEATURE REFERENCES
# =========================================================

feast_features = [
    f"karachi_aqi_features:{feature}"
    for feature in feature_names
]


# =========================================================
# GET LATEST FEATURES FROM FEAST
# =========================================================

print("\nRetrieving latest features from Feast...")

online_features = store.get_online_features(
    features=feast_features,
    entity_rows=[
        {"city": "Karachi"}
    ],
)

features_df = online_features.to_df()


# =========================================================
# DISPLAY FEATURES RETRIEVED
# =========================================================

print("\nFeatures retrieved from Feast:")
print(features_df.T)


# =========================================================
# PREPARE MODEL INPUT
# =========================================================

# Remove Feast entity column
X_latest = features_df.drop(
    columns=["city"]
)

# Reorder columns exactly as used during training
X_latest = X_latest[feature_names]


# =========================================================
# VERIFY INPUT
# =========================================================

print("\nModel input shape:", X_latest.shape)

print("\nFeature order matches training:")
print(
    list(X_latest.columns) == list(feature_names)
)


# =========================================================
# MAKE PREDICTION
# =========================================================

prediction = model.predict(X_latest)[0]


# =========================================================
# FINAL RESULT
# =========================================================

print("\n" + "=" * 60)
print("NEXT-DAY AQI PREDICTION")
print("=" * 60)

print(f"Predicted AQI: {prediction:.2f}")

print("\nPrediction pipeline:")
print(
    "Feast Online Store "
    "→ 21 Model Features "
    "→ Random Forest "
    "→ AQI Prediction"
)