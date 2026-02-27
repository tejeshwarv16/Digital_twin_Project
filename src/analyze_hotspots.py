# -*- coding: utf-8 -*-

import pandas as pd

LOG_FILE = "data/logs/vehicle_log.csv"

print("Loading log file...")
df = pd.read_csv(LOG_FILE)

print("Total rows:", len(df))

# ----------------------------
# Edge-level aggregation
# ----------------------------

print("\nAggregating by lane_id...")

lane_group = df.groupby("lane_id")

summary = lane_group.agg(
    avg_speed=("speed", "mean"),
    congestion_ratio=("speed", lambda x: (x < 1).mean()),
    violation_count=("violation_type", lambda x: (x != "none").sum()),
    total_samples=("vehicle_id", "count")
)

summary["violation_ratio"] = summary["violation_count"] / summary["total_samples"]

# Sort by congestion
top_congested = summary.sort_values("congestion_ratio", ascending=False).head(15)

print("\nTop 15 Most Congested Lanes:")
print(top_congested[[
    "avg_speed",
    "congestion_ratio",
    "violation_ratio"
]])

# Correlation analysis
correlation = summary["congestion_ratio"].corr(summary["violation_ratio"])

print("\nCorrelation between congestion and violation ratio:")
print(round(correlation, 4))

print("\nHotspot analysis complete.")