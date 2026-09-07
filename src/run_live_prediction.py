import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_PATH = PROJECT_ROOT / "src"

UPDATE_SCRIPT = SRC_PATH / "update_live_features.py"
PREDICTION_SCRIPT = SRC_PATH / "predict_from_feast.py"


def run_script(script_path):
    """
    Runs a Python script and stops the pipeline
    if that script fails.
    """

    print("\n" + "=" * 60)
    print(f"RUNNING: {script_path.name}")
    print("=" * 60 + "\n")

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=str(PROJECT_ROOT)
    )

    if result.returncode != 0:
        print("\n" + "=" * 60)
        print("PIPELINE FAILED")
        print("=" * 60)

        print(
            f"\nError occurred while running: "
            f"{script_path.name}"
        )

        sys.exit(result.returncode)


def main():

    print("\n" + "=" * 60)
    print("KARACHI LIVE AQI END-TO-END PREDICTION PIPELINE")
    print("=" * 60)

    # Step 1:
    # Fetch live data and update Feast
    run_script(UPDATE_SCRIPT)

    # Step 2:
    # Retrieve features from Feast and predict AQI
    run_script(PREDICTION_SCRIPT)

    print("\n" + "=" * 60)
    print("END-TO-END PIPELINE COMPLETED SUCCESSFULLY!")
    print("=" * 60)


if __name__ == "__main__":
    main()