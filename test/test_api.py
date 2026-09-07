from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app
from unittest.mock import patch


# ============================================================
# CREATE TEST CLIENT
# ============================================================

client = TestClient(app)


# ============================================================
# TEST HOME ENDPOINT
# ============================================================

def test_home():

    response = client.get(
        "/"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"

    assert "message" in data


# ============================================================
# TEST HEALTH ENDPOINT
# ============================================================

def test_health():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"

    assert (
        data["service"]
        == "Karachi AQI Forecasting API"
    )

# ============================================================
# TEST PREDICTION ENDPOINT
# ============================================================

@patch(
    "app.main.predict_aqi"
)
def test_predict(
    mock_predict
):

    # Fake prediction
    mock_predict.return_value = 61.63


    response = client.get(
        "/predict"
    )


    assert (
        response.status_code == 200
    )


    data = response.json()


    assert (
        data["city"] == "Karachi"
    )


    assert (
        data["predicted_aqi"] == 61.63
    )


    assert (
        data["aqi_category"]
        == "Moderate"
    )


    assert (
        data["prediction_for"]
        == "next day"
    )


    assert (
        data["model"]
        == "Random Forest"
    )


    assert (
        data["feature_store"]
        == "Feast"
    )


    assert (
        "timestamp" in data
    )

# ============================================================
# TEST READINESS ENDPOINT
# ============================================================

def test_ready():

    response = client.get(
        "/ready"
    )

    assert (
        response.status_code == 200
    )

    data = response.json()

    assert (
        data["status"] == "ready"
    )

    assert (
        data["model"] == "loaded"
    )

    assert (
        data["feature_store"]
        == "connected"
    )

    assert (
        data["features"]
        == "available"
    )

# ============================================================
# TEST READINESS FAILURE
# ============================================================

@patch(
    "app.main.get_latest_features"
)
def test_ready_failure(
    mock_features
):

    # Simulate Feast failure
    mock_features.side_effect = Exception(
        "Feast connection failed"
    )


    response = client.get(
        "/ready"
    )


    assert (
        response.status_code == 503
    )


    data = response.json()


    assert (
        data["detail"]["status"]
        == "not ready"
    )


    assert (
        "Feast connection failed"
        in data["detail"]["reason"]
    )