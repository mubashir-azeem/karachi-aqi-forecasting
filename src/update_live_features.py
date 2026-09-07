import sys
from pathlib import Path

import requests
import pandas as pd

from feast import FeatureStore


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)


HISTORICAL_DATA_PATH = (

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


# Allow importing modules from src

sys.path.insert(
    0,
    str(PROJECT_ROOT / "src")
)


from feature_engineering import create_features


# ============================================================
# CONFIGURATION
# ============================================================

from config import (

    CITY,

    LATITUDE,

    LONGITUDE,

    TIMEZONE,

    OPEN_METEO_BASE_URL,

)


# ============================================================
# MODEL FEATURE NAMES
# IMPORTANT:
# This order must match the training order
# ============================================================

FEATURE_NAMES = [

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


# ============================================================
# FETCH LIVE AIR QUALITY DATA
# ============================================================

def fetch_live_air_quality_data():

    print(
        "\nFetching latest live air quality data..."
    )


    hourly_variables = [

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

    ]


    params = {

        "latitude": LATITUDE,

        "longitude": LONGITUDE,

        "hourly": (
            ",".join(hourly_variables)
        ),

        "timezone": TIMEZONE,

        "domains": "cams_global",

        "past_days": 7,

        "forecast_days": 1,

    }


    response = requests.get(

        OPEN_METEO_BASE_URL,

        params=params,

        timeout=30,

    )


    response.raise_for_status()


    data = response.json()


    print(
        "Live API request successful!"
    )


    hourly_df = pd.DataFrame(
        data["hourly"]
    )


    hourly_df["time"] = pd.to_datetime(
        hourly_df["time"]
    )


    print(
        f"Hourly live data shape: "
        f"{hourly_df.shape}"
    )


    return hourly_df


# ============================================================
# CONVERT HOURLY DATA TO DAILY DATA
# ============================================================

def convert_hourly_to_daily(hourly_df):

    print(
        "\nConverting hourly data "
        "to daily averages..."
    )


    hourly_df = hourly_df.copy()


    hourly_df["date"] = (

        hourly_df["time"]

        .dt

        .normalize()

    )


    air_quality_columns = [

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

    ]


    daily_df = (

        hourly_df

        .groupby(
            "date"
        )[air_quality_columns]

        .mean()

        .reset_index()

    )


    print(
        f"Daily live data shape: "
        f"{daily_df.shape}"
    )


    print(
        "\nLatest live daily date:"
    )


    print(
        daily_df["date"].max()
    )


    return daily_df


# ============================================================
# LOAD HISTORICAL DATA
# ============================================================

def load_historical_data():

    print(
        "\nLoading historical data..."
    )


    historical_df = pd.read_csv(
        HISTORICAL_DATA_PATH
    )


    historical_df["date"] = pd.to_datetime(
        historical_df["date"]
    )


    print(
        f"Historical data shape: "
        f"{historical_df.shape}"
    )


    print(
        f"Historical data ends at: "
        f"{historical_df['date'].max()}"
    )


    return historical_df


# ============================================================
# COMBINE HISTORICAL + LIVE DATA
# ============================================================

def combine_data(

    historical_df,

    live_daily_df,

):

    print(
        "\nCombining historical "
        "and live data..."
    )


    combined_df = pd.concat(

        [

            historical_df,

            live_daily_df,

        ],

        ignore_index=True,

    )


    # Keep newest version
    # when dates overlap

    combined_df = (

        combined_df

        .sort_values(
            "date"
        )

        .drop_duplicates(

            subset=[
                "date"
            ],

            keep="last",

        )

        .reset_index(
            drop=True
        )

    )


    print(
        f"Combined data shape: "
        f"{combined_df.shape}"
    )


    print(
        f"Latest available date: "
        f"{combined_df['date'].max()}"
    )


    return combined_df


# ============================================================
# PREPARE LATEST FEATURES FOR FEAST
# ============================================================

def prepare_feast_features(
    processed_df,
):

    latest_row = (

        processed_df

        .tail(1)

        .copy()

    )


    latest_row = latest_row[

        ["date"]

        + FEATURE_NAMES

    ]


    latest_row.insert(

        0,

        "city",

        CITY,

    )


    latest_row = latest_row.rename(

        columns={

            "date":
            "event_timestamp"

        }

    )


    # Ensure correct
    # Feast data type

    latest_row[
        "event_timestamp"
    ] = pd.to_datetime(

        latest_row[
            "event_timestamp"
        ]

    )


    for column in FEATURE_NAMES:

        latest_row[
            column
        ] = (

            latest_row[
                column
            ]

            .astype(float)

        )


    print(
        "\nLatest feature record "
        "prepared for Feast:"
    )


    print(
        latest_row.T
    )


    return latest_row


# ============================================================
# PUSH FEATURES TO FEAST
# ============================================================

def push_to_feast(
    latest_features,
):

    print(
        "\nConnecting to Feast..."
    )


    store = FeatureStore(

        repo_path=str(
            FEATURE_REPO_PATH
        )

    )


    print(
        "Pushing latest features "
        "to Feast Online Store..."
    )


    store.push(

        push_source_name=
        "karachi_aqi_push_source",

        df=latest_features,

    )


    print(
        "\n"
        + "=" * 60
    )


    print(
        "LIVE FEATURES PUSHED "
        "TO FEAST SUCCESSFULLY!"
    )


    print(
        "=" * 60
    )


    print(
        f"\nCity: {CITY}"
    )


    print(
        f"Latest feature date: "

        f"{latest_features['event_timestamp'].iloc[0]}"

    )


    print(
        f"\nNumber of model features: "
        f"{len(FEATURE_NAMES)}"
    )


# ============================================================
# MAIN PIPELINE
# ============================================================

if __name__ == "__main__":

    print(

        "\n"
        + "=" * 60

    )


    print(
        f"{CITY.upper()} LIVE AQI "
        "FEATURE UPDATE PIPELINE"
    )


    print(
        "=" * 60
    )


    # Step 1:
    # Fetch live data

    hourly_df = (

        fetch_live_air_quality_data()

    )


    # Step 2:
    # Convert hourly → daily

    live_daily_df = (

        convert_hourly_to_daily(
            hourly_df
        )

    )


    # Step 3:
    # Load historical data

    historical_df = (

        load_historical_data()

    )


    # Step 4:
    # Combine data

    combined_df = (

        combine_data(

            historical_df,

            live_daily_df,

        )

    )


    # Step 5:
    # Create features

    print(
        "\nCreating 21 model features..."
    )


    processed_df = (

        create_features(
            combined_df
        )

    )


    print(
        f"Processed dataset shape: "
        f"{processed_df.shape}"
    )


    # Step 6:
    # Prepare Feast features

    latest_features = (

        prepare_feast_features(
            processed_df
        )

    )


    # Step 7:
    # Push to Feast

    push_to_feast(
        latest_features
    )


    print(

        "\n"
        + "=" * 60

    )


    print(
        "PIPELINE COMPLETED "
        "SUCCESSFULLY!"
    )


    print(
        "=" * 60
    )