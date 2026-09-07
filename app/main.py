from datetime import datetime

from fastapi import FastAPI, HTTPException

from app.schemas import (
    HealthResponse,
    PredictionResponse,
)

from app.logger import logger

from src.config import CITY

from src.prediction_service import (
    predict_aqi,
    get_latest_features,
)


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(

    title=f"{CITY} AQI Forecasting API",

    description=(
        f"Production API for predicting "
        f"next-day AQI in {CITY} using "
        f"Random Forest and Feast"
    ),

    version="1.1.0"

)


# ============================================================
# HOME ENDPOINT
# ============================================================

@app.get("/")
def home():

    logger.info(
        "Home endpoint accessed"
    )

    return {

        "message": (
            f"{CITY} AQI Forecasting "
            "API is running"
        ),

        "status": "success"

    }


# ============================================================
# HEALTH CHECK ENDPOINT
# ============================================================

@app.get(
    "/health",
    response_model=HealthResponse
)
def health_check():

    logger.info(
        "Health check requested"
    )

    return {

        "status": "healthy",

        "service": (
            f"{CITY} AQI Forecasting API"
        )

    }


# ============================================================
# READINESS CHECK ENDPOINT
# ============================================================

@app.get("/ready")
def readiness_check():

    try:

        logger.info(
            "Readiness check requested"
        )


        # ============================================
        # CHECK FEAST FEATURES
        # ============================================

        X_latest = (
            get_latest_features()
        )


        # ============================================
        # VERIFY FEATURES
        # ============================================

        if X_latest is None:

            raise ValueError(
                "Features are not available"
            )


        if len(X_latest) == 0:

            raise ValueError(
                "No feature records available"
            )


        # ============================================
        # API IS READY
        # ============================================

        logger.info(
            "API readiness check passed"
        )


        return {

            "status": "ready",

            "model": "loaded",

            "feature_store": "connected",

            "features": (
                "available"
            )

        }


    except Exception as e:

        logger.error(

            f"Readiness check failed: {str(e)}"
        )


        raise HTTPException(

            status_code=503,

            detail={

                "status": (
                    "not ready"
                ),

                "reason": str(e)

            }

        )


# ============================================================
# AQI CATEGORY FUNCTION
# ============================================================

def get_aqi_category(aqi: float):

    if aqi <= 50:

        return "Good"

    elif aqi <= 100:

        return "Moderate"

    elif aqi <= 150:

        return (
            "Unhealthy for Sensitive Groups"
        )

    elif aqi <= 200:

        return "Unhealthy"

    elif aqi <= 300:

        return "Very Unhealthy"

    else:

        return "Hazardous"


# ============================================================
# PREDICTION ENDPOINT
# ============================================================

@app.get(
    "/predict",
    response_model=PredictionResponse
)
def predict():

    try:

        logger.info(
            "Prediction request received"
        )


        # ============================================
        # GET REAL AQI PREDICTION
        # ============================================

        predicted_aqi = (
            predict_aqi()
        )


        # ============================================
        # ROUND PREDICTION
        # ============================================

        predicted_aqi = round(

            float(predicted_aqi),

            2

        )


        # ============================================
        # GET AQI CATEGORY
        # ============================================

        aqi_category = (
            get_aqi_category(
                predicted_aqi
            )
        )


        # ============================================
        # LOG RESULT
        # ============================================

        logger.info(

            f"Prediction completed | "

            f"AQI: {predicted_aqi} | "

            f"Category: {aqi_category}"

        )


        # ============================================
        # RETURN RESPONSE
        # ============================================

        return {

            "city": CITY,

            "predicted_aqi": (
                predicted_aqi
            ),

            "aqi_category": (
                aqi_category
            ),

            "prediction_for": (
                "next day"
            ),

            "model": (
                "Random Forest"
            ),

            "feature_store": (
                "Feast"
            ),

            "timestamp": (
                datetime.now().isoformat()
            )

        }


    except Exception as e:

        logger.error(

            f"Prediction failed: {str(e)}"
        )

        raise HTTPException(

            status_code=500,

            detail=(

                "Prediction service "
                "failed"

            )

        )