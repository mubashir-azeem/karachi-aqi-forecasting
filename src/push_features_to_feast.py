import sys
from pathlib import Path

import pandas as pd
from feast import FeatureStore
from feast.data_source import PushMode


# =========================================================
# PROJECT PATHS
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Add project root to Python path
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "air_quality"
    / "air_quality_historical.csv"
)

FEATURE_REPO_PATH = (
    PROJECT_ROOT
    / "feature_repo"
    / "feature_repo"
)


# =========================================================
# FEATURE ENGINEERING FUNCTION
# =========================================================

def create_features(data):
    """
    Creates the exact features required by the trained AQI model.
    """

    # Make a copy so original data is not changed
    data = data.copy()

    # Ensure date is datetime
    data["date"] = pd.to_datetime(data["date"])

    # Sort chronologically
    data = data.sort_values("date").reset_index(drop=True)

    # -----------------------------------------------------
    # 1. Time-based features
    # -----------------------------------------------------

    data["year"] = data["date"].dt.year
    data["month"] = data["date"].dt.month
    data["day"] = data["date"].dt.day
    data["day_of_week"] = data["date"].dt.dayofweek

    # -----------------------------------------------------
    # 2. Lag features
    # -----------------------------------------------------

    data["us_aqi_lag_1"] = data["us_aqi"].shift(1)

    data["us_aqi_lag_3"] = data["us_aqi"].shift(3)

    data["us_aqi_lag_7"] = data["us_aqi"].shift(7)

    # -----------------------------------------------------
    # 3. Rolling features
    # -----------------------------------------------------

    data["us_aqi_roll_3"] = (
        data["us_aqi"].rolling(3).mean()
    )

    data["us_aqi_roll_7"] = (
        data["us_aqi"].rolling(7).mean()
    )

    data["us_aqi_roll_std_7"] = (
        data["us_aqi"].rolling(7).std()
    )

    # Remove rows where lag or rolling
    # features cannot be calculated
    data = data.dropna().reset_index(drop=True)

    return data


# =========================================================
# LOAD HISTORICAL DATA
# =========================================================

print("\nLoading historical air quality data...")

df = pd.read_csv(DATA_PATH)

print("Raw dataset shape:", df.shape)


# =========================================================
# CREATE MODEL FEATURES
# =========================================================

processed_df = create_features(df)

print("\nFeature engineering completed.")
print("Processed data shape:", processed_df.shape)


# =========================================================
# MODEL FEATURE COLUMNS
# =========================================================

model_features = [
    "pm10",
    "pm2_5",
    "carbon_monoxide",
    "nitrogen_dioxide",
    "sulphur_dioxide",
    "ozone",
    "aerosol_optical_depth",
    "dust",
    "uv_index",
    "us_aqi",
    "european_aqi",
    "year",
    "month",
    "day",
    "day_of_week",
    "us_aqi_lag_1",
    "us_aqi_lag_3",
    "us_aqi_lag_7",
    "us_aqi_roll_3",
    "us_aqi_roll_7",
    "us_aqi_roll_std_7",
]


# =========================================================
# GET LATEST FEATURE RECORD
# =========================================================

latest_features = processed_df.iloc[[-1]].copy()


# =========================================================
# PREPARE DATA FOR FEAST
# =========================================================

# Feast entity key
latest_features["city"] = "Karachi"

# Feast requires an event timestamp
latest_features["event_timestamp"] = latest_features["date"]

# Keep only required columns
feast_columns = [
    "city",
    "event_timestamp",
] + model_features

latest_features = latest_features[feast_columns]


# =========================================================
# FIX DATA TYPES FOR FEAST
# =========================================================

# Integer features
integer_columns = [
    "year",
    "month",
    "day",
    "day_of_week",
]

# Floating-point features
float_columns = [
    "pm10",
    "pm2_5",
    "carbon_monoxide",
    "nitrogen_dioxide",
    "sulphur_dioxide",
    "ozone",
    "aerosol_optical_depth",
    "dust",
    "uv_index",
    "us_aqi",
    "european_aqi",
    "us_aqi_lag_1",
    "us_aqi_lag_3",
    "us_aqi_lag_7",
    "us_aqi_roll_3",
    "us_aqi_roll_7",
    "us_aqi_roll_std_7",
]


# Convert integer columns to int64
latest_features[integer_columns] = (
    latest_features[integer_columns].astype("int64")
)

# Convert numerical columns to float64
latest_features[float_columns] = (
    latest_features[float_columns].astype("float64")
)

# Ensure timestamp is datetime
latest_features["event_timestamp"] = pd.to_datetime(
    latest_features["event_timestamp"]
)

# Ensure city is string
latest_features["city"] = (
    latest_features["city"].astype(str)
)


# =========================================================
# DISPLAY DATA BEING PUSHED
# =========================================================

print("\nLatest features being pushed to Feast:")
print(latest_features.T)

print("\nData types:")
print(latest_features.dtypes)


# =========================================================
# CONNECT TO FEAST FEATURE STORE
# =========================================================

store = FeatureStore(
    repo_path=str(FEATURE_REPO_PATH)
)


# =========================================================
# PUSH FEATURES TO ONLINE STORE
# =========================================================

store.push(
    "karachi_aqi_push_source",
    latest_features,
    to=PushMode.ONLINE,
)


# =========================================================
# SUCCESS MESSAGE
# =========================================================

print("\n" + "=" * 60)
print("FEATURES PUSHED TO FEAST SUCCESSFULLY!")
print("=" * 60)

print("\nEntity:")
print("City: Karachi")

print("\nEvent timestamp:")
print(
    latest_features["event_timestamp"].iloc[0]
)

print("\nNumber of model features pushed:")
print(len(model_features))

print("\nDestination:")
print("Feast Online Store")