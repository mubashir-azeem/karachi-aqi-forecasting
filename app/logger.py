import logging


# ============================================================
# LOGGER CONFIGURATION
# ============================================================

logging.basicConfig(

    level=logging.INFO,

    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "%(message)s"
    )

)


logger = logging.getLogger(
    "karachi_aqi_api"
)