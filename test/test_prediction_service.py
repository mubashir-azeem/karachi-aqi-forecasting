from src.prediction_service import (
    get_latest_features,
    predict_aqi,
)


# ============================================================
# TEST FEAST FEATURES
# ============================================================

def test_get_latest_features():

    X_latest = (
        get_latest_features()
    )


    # Check features exist
    assert X_latest is not None


    # Check exactly one record
    assert len(X_latest) == 1


    # Check exactly 21 features
    assert X_latest.shape[1] == 21


# ============================================================
# TEST REAL AQI PREDICTION
# ============================================================

def test_real_prediction():

    prediction = (
        predict_aqi()
    )


    # Check prediction exists
    assert prediction is not None


    # Check prediction is numeric
    assert isinstance(
        prediction,
        float
    )


    # AQI cannot be negative
    assert prediction >= 0