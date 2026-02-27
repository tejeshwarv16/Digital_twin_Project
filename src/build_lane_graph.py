# -*- coding: utf-8 -*-

import traci
import os
import pandas as pd

NET_FILE = "data/sumo_network/hinjewadi_phase3.net.xml"
STATE_FILE = "data/processed/lane_time_tensor.csv"
OUTPUT_FILE = "data/processed/lane_graph_edges.csv"

print("Loading active lanes from state tensor...")
state_df = pd.read_csv(STATE_FILE)
active_lanes = set(state_df["lane_id"].unique())

print("Active lanes:", len(active_lanes))

print("Starting SUMO to extract lane connectivity...")
traci.start(["sumo", "-n", NET_FILE, "--quit-on-end"])

edges = []

for lane in active_lanes:
    try:
        links = traci.lane.getLinks(lane)

        for link in links:
            target_lane = link[0]

            # Only keep edges within active lane set
            if target_lane in active_lanes:
                edges.append((lane, target_lane))
    except:
        continue

traci.close()

df_edges = pd.DataFrame(edges, columns=["source_lane", "target_lane"])

os.makedirs("data/processed", exist_ok=True)
df_edges.to_csv(OUTPUT_FILE, index=False)

print(f"[PASS] Saved filtered lane graph to {OUTPUT_FILE}")
print("Filtered edge count:", len(df_edges))
print("Unique source lanes:", df_edges["source_lane"].nunique())
print("Unique target lanes:", df_edges["target_lane"].nunique())
print("Done.")