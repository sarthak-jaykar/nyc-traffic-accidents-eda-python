"""
Step 1: Ingest and profile the raw file. Reads only; does not change the data.
Prints profiling tables to the console.
"""
import pandas as pd
from common import RAW_FILE, RESULTS

def main():
    df = pd.read_csv(RAW_FILE, low_memory=False)
    summary = pd.DataFrame({
        "metric": ["rows", "columns", "full duplicate rows", "duplicate COLLISION_ID values",
                   "first CRASH DATE", "last CRASH DATE"],
        "value": [len(df), df.shape[1], int(df.duplicated().sum()),
                  int(df["COLLISION_ID"].duplicated().sum()),
                  pd.to_datetime(df["CRASH DATE"]).min().date(),
                  pd.to_datetime(df["CRASH DATE"]).max().date()],
    })
    print(summary.to_string(index=False))

    nulls = pd.DataFrame({
        "column": df.columns,
        "null_count": df.isna().sum().values,
        "null_pct": (100 * df.isna().mean()).round(2).values,
    })
    print(nulls.to_string(index=False))
    print(summary.to_string(index=False))
    print(nulls[nulls.null_count > 0].to_string(index=False))

if __name__ == "__main__":
    main()
