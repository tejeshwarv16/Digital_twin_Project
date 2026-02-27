# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import os

LOG_FILE = "data/logs/vehicle_log.csv"
OUTPUT_FILE = "data/processed/lane_time_tensor.csv"

FUTURE_DELTA = 10  # seconds ahead for prediction
CONGESTION_SPEED_THRESHOLD = 1.0  # m/s

print("Loading vehicle log...")
df = pd.read_csv(LOG_FILE)

print("Aggregating per lane per timestep...")

grouped = df.groupby(["time", "lane_id"]).agg(
    mean_speed=("speed", "mean"),
    vehicle_count=("vehicle_id", "count"),
    violation_rate=("violation_type", lambda x: (x != "none").mean())
).reset_index()

# Congestion ratio = 1 if slow, 0 otherwise
grouped["congestion_flag"] = (
    grouped["mean_speed"] < CONGESTION_SPEED_THRESHOLD
).astype(int)

# Ensure full time index per lane
print("Filling missing timesteps...")

all_times = np.arange(grouped["time"].min(), grouped["time"].max() + 1)
all_lanes = grouped["lane_id"].unique()

full_index = pd.MultiIndex.from_product(
    [all_times, all_lanes],
    names=["time", "lane_id"]
)

grouped = grouped.set_index(["time", "lane_id"])
grouped = grouped.reindex(full_index)

# Fill missing values
grouped["mean_speed"] = grouped["mean_speed"].fillna(0)
grouped["vehicle_count"] = grouped["vehicle_count"].fillna(0)
grouped["violation_rate"] = grouped["violation_rate"].fillna(0)
grouped["congestion_flag"] = grouped["congestion_flag"].fillna(0)

grouped = grouped.reset_index()

print("Computing future congestion labels...")

grouped["future_congestion"] = (
    grouped.groupby("lane_id")["congestion_flag"]
    .shift(-FUTURE_DELTA)
)

grouped["future_congestion"] = grouped["future_congestion"].fillna(0)

# Optional: remove last FUTURE_DELTA timesteps (no valid future)
max_time = grouped["time"].max()
grouped = grouped[grouped["time"] <= max_time - FUTURE_DELTA]

os.makedirs("data/processed", exist_ok=True)
grouped.to_csv(OUTPUT_FILE, index=False)

print(f"[PASS] Saved processed tensor to {OUTPUT_FILE}")
print(f"Total rows: {len(grouped)}")
print("Done.")