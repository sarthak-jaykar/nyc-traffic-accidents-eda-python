"""Helper to load the processed, feature-enriched file (used by analysis and charts)."""
import pandas as pd
from common import PROCESSED_FILE

def load_features() -> pd.DataFrame:
    return pd.read_csv(PROCESSED_FILE, low_memory=False, parse_dates=["crash_date"])
