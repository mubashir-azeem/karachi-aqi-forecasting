from pydantic import BaseModel


# ============================================================
# HEALTH RESPONSE MODEL
# ============================================================

class HealthResponse(BaseModel):

    status: str

    service: str


# ============================================================
# PREDICTION RESPONSE MODEL
# ============================================================

class PredictionResponse(BaseModel):

    city: str

    predicted_aqi: float

    aqi_category: str

    prediction_for: str

    model: str

    feature_store: str

    timestamp: str