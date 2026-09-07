from feast import FeatureStore


# --------------------------------------------------
# 1. Connect to the Feast feature repository
# --------------------------------------------------

store = FeatureStore(
    repo_path=r"D:\Projects\Karachi_AQI_Forecasting\feature_repo\feature_repo"
)


# --------------------------------------------------
# 2. Request features for Karachi
# --------------------------------------------------

features = store.get_online_features(
    features=[
        "karachi_aqi_features:pm10",
        "karachi_aqi_features:pm2_5",
        "karachi_aqi_features:us_aqi",
        "karachi_aqi_features:us_aqi_lag_1",
        "karachi_aqi_features:us_aqi_lag_3",
        "karachi_aqi_features:us_aqi_lag_7",
        "karachi_aqi_features:us_aqi_roll_3",
        "karachi_aqi_features:us_aqi_roll_7",
        "karachi_aqi_features:us_aqi_roll_std_7",
    ],
    entity_rows=[
        {"city": "Karachi"}
    ],
)


# --------------------------------------------------
# 3. Convert retrieved features into a DataFrame
# --------------------------------------------------

result = features.to_df()


# --------------------------------------------------
# 4. Display result
# --------------------------------------------------

print("\n" + "=" * 60)
print("FEATURES RETRIEVED FROM FEAST ONLINE STORE")
print("=" * 60)

print(result)

print("\nFeature retrieval successful!")