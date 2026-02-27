# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

LOG_FILE = "data/logs/vehicle_log.csv"

print("Loading data...")
df = pd.read_csv(LOG_FILE)

# Identify top 5 congested lanes
lane_summary = df.groupby("lane_id").agg(
    congestion_ratio=("speed", lambda x: (x < 1).mean())
)

top_lanes = lane_summary.sort_values(
    "congestion_ratio", ascending=False
).head(5).index.tolist()

print("\nTop 5 congested lanes:")
for lane in top_lanes:
    print(lane)

print("\nAnalyzing temporal causality per lane...\n")

for lane in top_lanes:

    lane_df = df[df["lane_id"] == lane]

    grouped = lane_df.groupby("time").agg(
        mean_speed=("speed", "mean"),
        violation_count=("violation_type", lambda x: (x != "none").sum()),
        vehicle_count=("vehicle_id", "count")
    )

    grouped["violation_rate"] = (
        grouped["violation_count"] / grouped["vehicle_count"]
    )

    grouped = grouped.dropna()

    # Skip if not enough data
    if len(grouped) < 50:
        print(f"\nLane {lane}: Not enough data")
        continue

    max_lag = 30
    best_lag = None
    best_corr = 0

    for lag in range(1, max_lag + 1):
        shifted_speed = grouped["mean_speed"].shift(-lag)
        corr = grouped["violation_rate"].corr(shifted_speed)

        if abs(corr) > abs(best_corr):
            best_corr = corr
            best_lag = lag

    print(f"\nLane: {lane}")
    print(f"  Best Lag: {best_lag} seconds")
    print(f"  Lag Correlation: {round(best_corr, 4)}")