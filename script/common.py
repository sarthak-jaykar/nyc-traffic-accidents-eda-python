"""Shared paths and helpers for the NYC accidents project."""
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW_FILE = ROOT / "data" / "nyc_accidents_2020.csv"
PROCESSED_FILE = Path(tempfile.gettempdir()) / "collisions_clean.csv"
RESULTS = ROOT / "results"
SCREENSHOTS = ROOT / "screenshots"

RESULTS.mkdir(parents=True, exist_ok=True)
SCREENSHOTS.mkdir(parents=True, exist_ok=True)

# Days in each month covered by the data (the file ends on 29 Aug 2020)
DAYS_IN_PERIOD = {1: 31, 2: 29, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 29}
MONTH_NAMES = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 7: "Jul", 8: "Aug"}


def load_features():
    """Load the feature-enriched processed file (written by 03_features.py)."""
    import pandas as pd
    return pd.read_csv(PROCESSED_FILE, low_memory=False, parse_dates=["crash_date"])
