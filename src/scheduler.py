import time
import subprocess
import sys

from pathlib import Path

from config import (
    CITY,
    SCHEDULER_INTERVAL_HOURS,
)


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)


UPDATE_SCRIPT = (
    PROJECT_ROOT
    / "src"
    / "update_live_features.py"
)


# ============================================================
# UPDATE INTERVAL
# ============================================================

UPDATE_INTERVAL = (
    SCHEDULER_INTERVAL_HOURS
    * 60
    * 60
)


# ============================================================
# RUN FEATURE UPDATE
# ============================================================

def update_features():

    print(
        "\n"
        + "=" * 60
    )

    print(
        "RUNNING AUTOMATIC "
        "FEATURE UPDATE"
    )

    print(
        "=" * 60
        + "\n"
    )


    result = subprocess.run(
        [
            sys.executable,
            str(UPDATE_SCRIPT),
        ],
        cwd=str(PROJECT_ROOT),
    )


    if result.returncode != 0:

        print(
            "\nFEATURE UPDATE FAILED"
        )

    else:

        print(
            "\nFEATURE UPDATE "
            "COMPLETED SUCCESSFULLY"
        )


# ============================================================
# SCHEDULER
# ============================================================

def main():

    print(
        "\n"
        + "=" * 60
    )

    print(
        f"{CITY.upper()} AQI "
        "FEATURE SCHEDULER STARTED"
    )

    print(
        "=" * 60
    )


    print(
        "\nUpdate interval:"
    )

    print(
        f"Every "
        f"{SCHEDULER_INTERVAL_HOURS} hours"
    )


    # Run immediately when
    # scheduler starts

    update_features()


    # Keep scheduler running

    while True:

        print(
            "\nWaiting for next "
            "feature update..."
        )


        time.sleep(
            UPDATE_INTERVAL
        )


        update_features()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    main()