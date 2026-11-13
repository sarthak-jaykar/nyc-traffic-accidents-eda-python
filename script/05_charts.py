"""
Step 5: Charts. Each chart shows its source and the period covered.
Saves PNG files to screenshots/.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from common import RESULTS, SCREENSHOTS, PROCESSED_FILE
from common import load_features

SOURCE = "Source: NYC Accidents 2020 (1 Jan to 29 Aug 2020). Analysis in this project."

def save(fig, name):
    fig.tight_layout()
    fig.savefig(SCREENSHOTS / name, dpi=120)
    plt.close(fig)

def main():
    df = load_features()

    monthly = pd.read_csv(RESULTS / "q1_monthly.csv")
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(monthly["month_name"], monthly["collisions_per_day"], color="#3b6ea8")
    ax.set_title("Collisions per day by month, 2020")
    ax.set_ylabel("Collisions per day")
    ax.set_xlabel("Month (Aug covers 1 to 29 Aug)")
    for x, y in zip(monthly["month_name"], monthly["collisions_per_day"]):
        ax.text(x, y + 2, f"{y:.0f}", ha="center", fontsize=8)
    fig.text(0.01, 0.01, SOURCE, fontsize=7)
    save(fig, "q1_collisions_per_day_by_month.png")

    fig, ax = plt.subplots(figsize=(8, 4.5))
    hours = df["crash_hour"].value_counts().sort_index()
    ax.bar(hours.index, hours.values, color="#3b6ea8")
    ax.set_title("Collisions by hour of day (all months)")
    ax.set_xlabel("Hour (0 to 23)")
    ax.set_ylabel("Collisions")
    ax.set_xticks(range(0, 24, 2))
    fig.text(0.01, 0.01, SOURCE, fontsize=7)
    save(fig, "q1_collisions_by_hour.png")

    boroughs = pd.read_csv(RESULTS / "q2_borough.csv")
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.barh(boroughs["borough"][::-1], boroughs["collisions"][::-1], color="#3b6ea8")
    ax.set_title("Collisions by borough (Not recorded shown separately)")
    ax.set_xlabel("Collisions")
    fig.text(0.01, 0.01, SOURCE, fontsize=7)
    save(fig, "q2_collisions_by_borough.png")

    factors = pd.read_csv(RESULTS / "q3_factors_top.csv").head(10)
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.barh(factors["factor"][::-1], factors["collisions"][::-1], color="#3b6ea8")
    ax.set_title("Top primary contributing factors (vehicle 1)")
    ax.set_xlabel("Collisions")
    ax.tick_params(axis="y", labelsize=8)
    fig.text(0.01, 0.01, SOURCE + " 'Unspecified' is a recorded value, not an error.", fontsize=7)
    save(fig, "q3_top_factors.png")

    users = pd.read_csv(RESULTS / "q4_road_users.csv")
    fig, ax = plt.subplots(figsize=(7, 4.5))
    x = range(len(users))
    ax.bar([i - 0.2 for i in x], users["injured"], width=0.4, label="Injured", color="#3b6ea8")
    ax.bar([i + 0.2 for i in x], users["killed"], width=0.4, label="Killed", color="#b5483a")
    ax.set_xticks(list(x))
    ax.set_xticklabels(users["road_user"])
    ax.set_title("Injured and killed by road user type")
    ax.legend()
    fig.text(0.01, 0.01, SOURCE, fontsize=7)
    save(fig, "q4_road_users.png")

    fig, ax = plt.subplots(figsize=(9, 4.5))
    daily = df.groupby(["month", "crash_date"]).size().reset_index(name="collisions")
    daily["month_name"] = daily["month"].map({1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 7: "Jul", 8: "Aug"})
    order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug"]
    sns.boxplot(data=daily, x="month_name", y="collisions", order=order, ax=ax, color="#9bb7d4")
    ax.set_title("Daily collision counts by month (distribution across days)")
    ax.set_xlabel("Month")
    ax.set_ylabel("Collisions per day")
    fig.text(0.01, 0.01, SOURCE, fontsize=7)
    save(fig, "q6_daily_distribution_by_month.png")
    print("Charts saved to", SCREENSHOTS)

if __name__ == "__main__":
    main()
