# -*- coding: utf-8 -*-
"""
Created on Sat Feb 28 00:10:59 2026

@author: tejes
"""

import os
import osmnx as ox

# Tighter bounding box around Hinjewadi Phase 3
north = 18.585
south = 18.565
east = 73.700
west = 73.675

print("Downloading road network from OpenStreetMap...")

bbox = (north, south, east, west)

G = ox.graph_from_bbox(
    bbox=bbox,
    network_type="drive"
)

os.makedirs("data/raw_osm", exist_ok=True)

osm_file = "data/raw_osm/hinjewadi_phase3.osm"

ox.save_graph_xml(G, osm_file)

print(f"OSM network saved to {osm_file}")