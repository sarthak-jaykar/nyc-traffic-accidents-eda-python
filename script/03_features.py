"""
Step 3: Feature engineering on the cleaned file.

Time bands (crash hour):
  Night 00-05 | Morning peak 06-09 | Midday 10-15 | Evening peak 16-19 | Late evening 20-23
Flags:
  any_injury = persons_injured > 0 ; any_fatality = persons_killed > 0 ; any_casualty = either
Vulnerable road users (pedestrians, cyclists) are counted separately from motorists.
"""
import pandas as pd
from common import PROCESSED_FILE

TIME_BANDS = [(0, 5, "Night (00-05)"), (6, 9, "Morning peak (06-09)"), (10, 15, "Midday (10-15)"),
              (16, 19, "Evening peak (16-19)"), (20, 23, "Late evening (20-23)")]

def time_band(hour):
    for lo, hi, label in TIME_BANDS:
        if lo <= hour <= hi:
            return label
    return "Unknown"

def build_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["crash_date"] = pd.to_datetime(df["crash_date"])
    df["month"] = df["crash_date"].dt.month
    df["weekday"] = df["crash_date"].dt.day_name()
    df["weekday_num"] = df["crash_date"].dt.dayofweek
    df["time_band"] = df["crash_hour"].apply(time_band)
    df["any_injury"] = df["persons_injured"] > 0
    df["any_fatality"] = df["persons_killed"] > 0
    df["any_casualty"] = df["any_injury"] | df["any_fatality"]
    df["pedestrians_and_cyclists_injured"] = (df["number_of_pedestrians_injured"]
                                              + df["number_of_cyclist_injured"])
    df["pedestrians_and_cyclists_killed"] = (df["number_of_pedestrians_killed"]
                                             + df["number_of_cyclist_killed"])
    return df

def main():
    df = pd.read_csv(PROCESSED_FILE, low_memory=False, parse_dates=["crash_date"])
    feat = build_features(df)
    feat.to_csv(PROCESSED_FILE, index=False)
    print("Features added. Time band counts:")
    print(feat["time_band"].value_counts().to_string())

if __name__ == "__main__":
    main()
