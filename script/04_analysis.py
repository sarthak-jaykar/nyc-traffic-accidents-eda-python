"""
Step 4: Analysis for questions Q1 to Q6 (see documentation/01_business_brief.md).
Writes one CSV per output to results/.
Rates are shown per collision and per day, because raw counts are not comparable across months of different length.
"""
import pandas as pd
from scipy import stats
from common import PROCESSED_FILE, RESULTS, DAYS_IN_PERIOD, MONTH_NAMES
from common import load_features

def q1_time_patterns(df):
    monthly = (df.groupby("month").agg(collisions=("collision_id", "size"),
                                       injured_collisions=("any_injury", "sum"),
                                       killed=("persons_killed", "sum"),
                                       injured=("persons_injured", "sum"))
               .reset_index())
    monthly["days"] = monthly["month"].map(DAYS_IN_PERIOD)
    monthly["collisions_per_day"] = (monthly["collisions"] / monthly["days"]).round(1)
    monthly["injury_rate_pct"] = (100 * monthly["injured_collisions"] / monthly["collisions"]).round(2)
    monthly["month_name"] = monthly["month"].map(MONTH_NAMES)
    monthly.to_csv(RESULTS / "q1_monthly.csv", index=False)

    weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    wd = df.groupby("weekday").agg(collisions=("collision_id", "size"), injured=("persons_injured", "sum")).reindex(weekday_order)
    wd.to_csv(RESULTS / "q1_weekday.csv")

    bands = df.groupby("time_band").agg(collisions=("collision_id", "size"),
                                        injury_rate_pct=("any_injury", lambda s: round(100 * s.mean(), 2)),
                                        fatal_collisions=("any_fatality", "sum")).reset_index()
    bands.to_csv(RESULTS / "q1_time_bands.csv", index=False)
    return monthly

def q2_boroughs(df):
    b = df.groupby("borough").agg(collisions=("collision_id", "size"),
                                  injured=("persons_injured", "sum"),
                                  killed=("persons_killed", "sum"),
                                  injury_rate_pct=("any_injury", lambda s: round(100 * s.mean(), 2)),
                                  fatal_collisions=("any_fatality", "sum")).reset_index()
    b["share_of_collisions_pct"] = (100 * b["collisions"] / len(df)).round(2)
    b = b.sort_values("collisions", ascending=False)
    b.to_csv(RESULTS / "q2_borough.csv", index=False)
    return b

def q3_factors(df):
    known = df[~df["factor_unspecified"] & (df["factor_1"] != "Not recorded")]
    top = (df["factor_1"].value_counts().rename_axis("factor").reset_index(name="collisions").head(12))
    top["share_pct_all"] = (100 * top["collisions"] / len(df)).round(2)
    top["share_pct_specified_only"] = (100 * top["collisions"] / len(known)).round(2)
    top.loc[top["factor"].str.contains("Unspecified"), "share_pct_specified_only"] = None
    top.to_csv(RESULTS / "q3_factors_top.csv", index=False)

    inj = (known.groupby("factor_1").agg(collisions=("collision_id", "size"),
                                         injury_rate_pct=("any_injury", lambda s: round(100 * s.mean(), 2)),
                                         fatal_collisions=("any_fatality", "sum"))
           .sort_values("collisions", ascending=False).head(12).reset_index())
    inj.to_csv(RESULTS / "q3_factors_injury_rate.csv", index=False)
    return top, inj

def q4_road_users(df):
    rows = [
        ("Motorists", df["number_of_motorist_injured"].sum(), df["number_of_motorist_killed"].sum()),
        ("Pedestrians", df["number_of_pedestrians_injured"].sum(), df["number_of_pedestrians_killed"].sum()),
        ("Cyclists", df["number_of_cyclist_injured"].sum(), df["number_of_cyclist_killed"].sum()),
    ]
    users = pd.DataFrame(rows, columns=["road_user", "injured", "killed"])
    users["share_of_injured_pct"] = (100 * users["injured"] / users["injured"].sum()).round(2)
    users["share_of_killed_pct"] = (100 * users["killed"] / users["killed"].sum()).round(2)
    users.to_csv(RESULTS / "q4_road_users.csv", index=False)
    return users

def q5_streets(df):
    s = df[df["on_street_name"].notna()]
    top = (s.groupby("on_street_name").agg(collisions=("collision_id", "size"),
                                           injured=("persons_injured", "sum"),
                                           killed=("persons_killed", "sum"))
           .sort_values(["collisions", "injured"], ascending=False).head(15).reset_index())
    top.to_csv(RESULTS / "q5_top_streets.csv", index=False)
    missing_street = int(df["on_street_name"].isna().sum())
    return top, missing_street

def q6_daily_shift(df):
    """Daily collision counts in two periods. Test: Mann-Whitney U (non-parametric).
    Caveat: daily counts are not fully independent (weekday pattern, weather) and there is no 2019 baseline."""
    daily = df.groupby("crash_date").size().rename("collisions").reset_index()
    daily["month"] = daily["crash_date"].dt.month
    early = daily[daily["month"].isin([1, 2])]["collisions"]
    late = daily[daily["month"].isin([4, 5, 6])]["collisions"]
    stat, p = stats.mannwhitneyu(early, late, alternative="two-sided")
    out = pd.DataFrame([{
        "period_a": "Jan-Feb 2020", "days_a": len(early), "mean_per_day_a": round(early.mean(), 1),
        "period_b": "Apr-Jun 2020", "days_b": len(late), "mean_per_day_b": round(late.mean(), 1),
        "mann_whitney_u": stat, "p_value": float(f"{p:.3g}"),
        "change_pct": round(100 * (late.mean() - early.mean()) / early.mean(), 1),
    }])
    out.to_csv(RESULTS / "q6_period_comparison.csv", index=False)
    return out

def extreme_records(df):
    """Outlier investigation: records with the highest casualty counts. Reported, not removed."""
    ext = df.nlargest(10, "persons_injured")[["collision_id", "crash_date", "crash_time", "borough",
                                              "on_street_name", "persons_injured", "persons_killed", "factor_1"]]
    ext.to_csv(RESULTS / "outliers_top_injury_records.csv", index=False)
    return ext

def main():
    df = load_features()
    monthly = q1_time_patterns(df)
    borough = q2_boroughs(df)
    top, _ = q3_factors(df)
    users = q4_road_users(df)
    streets, missing_street = q5_streets(df)
    shift = q6_daily_shift(df)
    ext = extreme_records(df)
    print("Q1 monthly\n", monthly[["month_name", "collisions", "collisions_per_day", "injury_rate_pct"]].to_string(index=False))
    print("\nQ2 boroughs\n", borough.to_string(index=False))
    print("\nQ3 top factors\n", top.head(6).to_string(index=False))
    print("\nQ4 road users\n", users.to_string(index=False))
    print("\nQ5 streets (missing street name:", missing_street, ")\n", streets.head(6).to_string(index=False))
    print("\nQ6 period comparison\n", shift.to_string(index=False))
    print("\nOutliers\n", ext.head(3).to_string(index=False))

if __name__ == "__main__":
    main()
