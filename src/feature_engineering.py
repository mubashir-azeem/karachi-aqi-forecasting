import pandas as pd
import numpy as np


def create_features(data):
    """
    Creates the exact features required by the trained AQI model.
    """

    # Make a copy so the original data is not changed
    data = data.copy()

    # Ensure date is datetime
    data["date"] = pd.to_datetime(data["date"])

    # Sort chronologically
    data = data.sort_values("date").reset_index(drop=True)

    # -----------------------------
    # 1. Time-based features
    # -----------------------------
    data["year"] = data["date"].dt.year
    data["month"] = data["date"].dt.month
    data["day"] = data["date"].dt.day
    data["day_of_week"] = data["date"].dt.dayofweek

    # -----------------------------
    # 2. Lag features
    # -----------------------------
    data["us_aqi_lag_1"] = data["us_aqi"].shift(1)
    data["us_aqi_lag_3"] = data["us_aqi"].shift(3)
    data["us_aqi_lag_7"] = data["us_aqi"].shift(7)

    # -----------------------------
    # 3. Rolling features
    # -----------------------------
    data["us_aqi_roll_3"] = data["us_aqi"].rolling(3).mean()

    data["us_aqi_roll_7"] = data["us_aqi"].rolling(7).mean()

    data["us_aqi_roll_std_7"] = data["us_aqi"].rolling(7).std()

    # -----------------------------
    # Remove rows where lag/rolling
    # features cannot be calculated
    # -----------------------------
    data = data.dropna().reset_index(drop=True)

    return data