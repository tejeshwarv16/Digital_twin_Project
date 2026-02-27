# -*- coding: utf-8 -*-

import sumolib

NET_FILE = "data/sumo_network/hinjewadi_phase3.net.xml"

net = sumolib.net.readNet(NET_FILE)

print("Listing drivable edges...\n")

edges = []

for edge in net.getEdges():
    # skip internal edges (junction connectors)
    if not edge.isSpecial():
        edges.append(edge.getID())

print(f"Total usable edges: {len(edges)}\n")

# Print first 20 edges
for e in edges[:20]:
    print(e)