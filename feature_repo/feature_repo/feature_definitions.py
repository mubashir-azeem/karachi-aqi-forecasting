from datetime import timedelta

from feast import (
    Entity,
    FeatureView,
    Field,
    FileSource,
    PushSource,
    FeatureService,
    ValueType,
)

from feast.types import Float64


# ============================================================
# 1. ENTITY
# ============================================================

city = Entity(
    name="city",
    join_keys=["city"],
    value_type=ValueType.STRING,
    description="City for AQI data",
)


# ============================================================
# 2. HISTORICAL / BATCH DATA SOURCE
# ============================================================

karachi_aqi_batch_source = FileSource(
    name="karachi_aqi_batch_source",

    path=r"D:\Projects\Karachi_AQI_Forecasting\data\raw\air_quality\air_quality_historical.csv",

    timestamp_field="event_timestamp",
)


# ============================================================
# 3. PUSH SOURCE
# ============================================================

karachi_aqi_push_source = PushSource(
    name="karachi_aqi_push_source",

    batch_source=karachi_aqi_batch_source,
)


# ============================================================
# 4. FEATURE VIEW
# ============================================================

karachi_aqi_features = FeatureView(
    name="karachi_aqi_features",

    entities=[city],

    ttl=timedelta(days=7),

    schema=[
        # Air pollutant features
        Field(name="pm10", dtype=Float64),
        Field(name="pm2_5", dtype=Float64),
        Field(name="carbon_monoxide", dtype=Float64),
        Field(name="nitrogen_dioxide", dtype=Float64),
        Field(name="sulphur_dioxide", dtype=Float64),
        Field(name="ozone", dtype=Float64),
        Field(name="aerosol_optical_depth", dtype=Float64),
        Field(name="dust", dtype=Float64),
        Field(name="uv_index", dtype=Float64),

        # AQI features
        Field(name="us_aqi", dtype=Float64),
        Field(name="european_aqi", dtype=Float64),

        # Date features
        Field(name="year", dtype=Float64),
        Field(name="month", dtype=Float64),
        Field(name="day", dtype=Float64),
        Field(name="day_of_week", dtype=Float64),

        # Lag features
        Field(name="us_aqi_lag_1", dtype=Float64),
        Field(name="us_aqi_lag_3", dtype=Float64),
        Field(name="us_aqi_lag_7", dtype=Float64),

        # Rolling features
        Field(name="us_aqi_roll_3", dtype=Float64),
        Field(name="us_aqi_roll_7", dtype=Float64),
        Field(name="us_aqi_roll_std_7", dtype=Float64),
    ],

    source=karachi_aqi_push_source,

    online=True,

    tags={
        "city": "Karachi",
        "country": "Pakistan",
        "forecast_horizon": "1_day",
        "model": "Random_Forest",
    },
)


# ============================================================
# 5. FEATURE SERVICE
# ============================================================

karachi_aqi_prediction_service = FeatureService(
    name="karachi_aqi_prediction_service",

    features=[
        karachi_aqi_features,
    ],
)