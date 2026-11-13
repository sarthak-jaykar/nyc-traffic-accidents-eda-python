"""
Step 2: Clean and validate. Missing values are NOT filled; they are flagged and reported.

Rules:
- CRASH DATE / CRASH TIME parsed to a timestamp and an hour.
- Coordinates equal to 0 are invalid (no real NYC location has longitude 0), so they are set to missing.
- BOROUGH missing is kept as "Not recorded" and flagged; it is never guessed.
- CONTRIBUTING FACTOR "Unspecified" is kept as its own category and flagged.
- Casualty totals are taken from the source columns, checked for consistency with the per-user-type columns.
"""
import numpy as np
import pandas as pd
from common import RAW_FILE, PROCESSED_FILE, RESULTS

def main():
    df = pd.read_csv(RAW_FILE, low_memory=False)
    df = df.rename(columns=lambda c: c.strip().lower().replace(" ", "_"))

    df["crash_date"] = pd.to_datetime(df["crash_date"], errors="raise")
    df["crash_time"] = pd.to_datetime(df["crash_time"], format="%H:%M:%S", errors="raise")
    df["crash_hour"] = df["crash_time"].dt.hour
    df["crash_time"] = df["crash_time"].dt.strftime("%H:%M:%S")

    zero_coords = (df["latitude"] == 0) | (df["longitude"] == 0)
    missing_coords = df["latitude"].isna() | df["longitude"].isna()
    df["coords_missing"] = missing_coords
    df["coords_zero_invalid"] = zero_coords
    df.loc[zero_coords, ["latitude", "longitude"]] = np.nan

    df["borough_missing"] = df["borough"].isna()
    df["borough"] = df["borough"].fillna("Not recorded")

    df["factor_1"] = df["contributing_factor_vehicle_1"].fillna("Not recorded")
    df["factor_unspecified"] = df["factor_1"].str.contains("Unspecified", case=False)

    df["persons_injured"] = df["number_of_persons_injured"].astype(int)
    df["persons_killed"] = df["number_of_persons_killed"].astype(int)

    # Consistency: injured persons must be at least the sum of injured users by type
    by_type_injured = (df["number_of_pedestrians_injured"] + df["number_of_cyclist_injured"]
                       + df["number_of_motorist_injured"])
    by_type_killed = (df["number_of_pedestrians_killed"] + df["number_of_cyclist_killed"]
                      + df["number_of_motorist_killed"])
    df["casualty_check_ok"] = (df["persons_injured"] >= by_type_injured) & (df["persons_killed"] >= by_type_killed)

    df.to_csv(PROCESSED_FILE, index=False)

    checks = pd.DataFrame({
        "check": ["rows after cleaning", "coordinates missing in source", "coordinates equal to 0 (set to missing)",
                  "borough not recorded", "primary factor Unspecified", "casualty consistency failures",
                  "collision IDs unique"],
        "value": [len(df), int(df["coords_missing"].sum()), int(df["coords_zero_invalid"].sum()),
                  int(df["borough_missing"].sum()),
                  int(df["factor_unspecified"].sum()), int((~df["casualty_check_ok"]).sum()),
                  bool(df["collision_id"].is_unique)],
    })
    print(checks.to_string(index=False))
    print(checks.to_string(index=False))

if __name__ == "__main__":
    main()
