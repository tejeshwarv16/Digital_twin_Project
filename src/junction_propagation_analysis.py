# -*- coding: utf-8 -*-

import pandas as pd
import traci
import numpy as np
import os

NET_FILE = "data/sumo_network/hinjewadi_phase3.net.xml"
LOG_FILE = "data/logs/vehicle_log.csv"

print("Loading SUMO network...")
traci.start(["sumo", "-n", NET_FILE, "--quit-on-end"])

junctions = traci.junction.getIDList()

junction_map = {}

for j in junctions:
    incoming = traci.junction.getIncomingEdges(j)
    outgoing = traci.junction.getOutgoingEdges(j)

    incoming_lanes = []
    outgoing_lanes = []

    for edge in incoming:
        for i in range(traci.edge.getLaneNumber(edge)):
            incoming_lanes.append(f"{edge}_{i}")

    for edge in outgoing:
        for i in range(traci.edge.getLaneNumber(edge)):
            outgoing_lanes.append(f"{edge}_{i}")

    if incoming_lanes and outgoing_lanes:
        junction_map[j] = {
            "incoming": incoming_lanes,
            "outgoing": outgoing_lanes
        }

traci.close()

print("Loading log file...")
df = pd.read_csv(LOG_FILE)

results = []

print("\nAnalyzing junction propagation...\n")

for j, lanes in junction_map.items():

    inc_df = df[df["lane_id"].isin(lanes["incoming"])]
    out_df = df[df["lane_id"].isin(lanes["outgoing"])]

    # Lower threshold dramatically
    if len(inc_df) < 100 or len(out_df) < 100:
        continue

    inc_group = inc_df.groupby("time").agg(
        violation_rate=("violation_type", lambda x: (x != "none").mean())
    )

    out_group = out_df.groupby("time").agg(
        congestion_ratio=("speed", lambda x: (x < 1).mean())
    )

    merged = inc_group.join(out_group, how="inner").dropna()

    if len(merged) < 30:
        continue

    max_lag = 30
    best_lag = None
    best_corr = 0

    for lag in range(1, max_lag + 1):
        shifted_cong = merged["congestion_ratio"].shift(-lag)
        corr = merged["violation_rate"].corr(shifted_cong)

        if abs(corr) > abs(best_corr):
            best_corr = corr
            best_lag = lag

    results.append({
        "junction": j,
        "best_lag": best_lag,
        "correlation": best_corr
    })

if not results:
    print("No qualifying junctions found.")
else:
    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values("correlation")

    print("\nTop 10 Strongest Negative Propagation Signals:\n")
    print(results_df.head(10))

    os.makedirs("results", exist_ok=True)
    results_df.to_csv("results/junction_propagation_results.csv", index=False)
    print("\nSaved to results/junction_propagation_results.csv")

print("\nPropagation analysis complete.")