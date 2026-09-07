import os

from dotenv import load_dotenv


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# LOCATION CONFIGURATION
# ============================================================

CITY = os.getenv(
    "CITY",
    "Karachi"
)

COUNTRY = os.getenv(
    "COUNTRY",
    "Pakistan"
)


LATITUDE = float(
    os.getenv(
        "LATITUDE",
        "24.8607"
    )
)

LONGITUDE = float(
    os.getenv(
        "LONGITUDE",
        "67.0011"
    )
)


TIMEZONE = os.getenv(
    "TIMEZONE",
    "Asia/Karachi"
)


# ============================================================
# API CONFIGURATION
# ============================================================

OPEN_METEO_BASE_URL = os.getenv(
    "OPEN_METEO_BASE_URL",
    "https://air-quality-api.open-meteo.com/v1/air-quality"
)


# ============================================================
# SCHEDULER CONFIGURATION
# ============================================================

SCHEDULER_INTERVAL_HOURS = int(
    os.getenv(
        "SCHEDULER_INTERVAL_HOURS",
        "6"
    )
)