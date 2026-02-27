# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

df = pd.read_csv("./data/logs/vehicle_log.csv")

grouped = df.groupby("time")

per_step = grouped.agg(
    mean_speed=("speed", "mean"),
    violation_count=("violation_type", lambda x: (x != "none").sum()),
    vehicle_count=("vehicle_id", "count")
)

# Safe division
per_step["violation_rate"] = per_step["violation_count"] / per_step["vehicle_count"]
per_step = per_step.dropna()

print("Mean violation rate:", per_step["violation_rate"].mean())

# Instantaneous correlation
corr = per_step["violation_rate"].corr(per_step["mean_speed"])
print("Instantaneous correlation:", corr)

# Lag correlation
max_lag = 30
best_lag = None
best_corr = 0

for lag in range(1, max_lag + 1):
    shifted_speed = per_step["mean_speed"].shift(-lag)
    c = per_step["violation_rate"].corr(shifted_speed)
    if abs(c) > abs(best_corr):
        best_corr = c
        best_lag = lag

print("Best lag:", best_lag)
print("Lag correlation:", best_corr)

import pandas as pd

df = pd.read_csv("data/processed/lane_time_tensor.csv")

print("Unique timesteps:", df["time"].nunique())
print("Unique lanes:", df["lane_id"].nunique())
print("Future congestion rate:", df["future_congestion"].mean())


import pandas as pd

edges = pd.read_csv("data/processed/lane_graph_edges.csv")

all_lanes = set(pd.read_csv("data/processed/lane_time_tensor.csv")["lane_id"].unique())

connected_lanes = set(edges["source_lane"]).union(set(edges["target_lane"]))

isolated = all_lanes - connected_lanes

print("Isolated lanes:", len(isolated))