# -*- coding: utf-8 -*-
"""
Created on Sat Feb 28 00:10:59 2026

@author: tejes
"""

import os
import time
import osmnx as ox

# Increase Overpass area limit (IMPORTANT)
ox.settings.overpass_max_query_area_size = 50_000_000

def main():
    north = 18.585
    south = 18.565
    east = 73.700
    west = 73.675
    
    bbox = (north, south, east, west)
    
    print("\nStarting Hinjewadi Phase 3 extraction...")
    start_time = time.time()
    
    G = ox.graph_from_bbox(
        bbox=bbox,
        network_type="drive"
    )
    
    elapsed = time.time() - start_time
    print(f"\nDownload completed in {elapsed:.2f} seconds.")
    
    print(f"[PASS] Graph contains {len(G.nodes)} nodes and {len(G.edges)} edges.")
    
    os.makedirs("data/raw_osm", exist_ok=True)
    osm_file = "data/raw_osm/hinjewadi_phase3.osm"
    
    ox.save_graph_xml(G, osm_file)
    
    print("File saved successfully.")
    print("\nExtraction process completed.\n")


if __name__ == "__main__":
    main()