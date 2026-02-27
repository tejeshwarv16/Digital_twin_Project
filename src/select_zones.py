# -*- coding: utf-8 -*-


import sumolib

NET_FILE = "data/sumo_network/hinjewadi_phase3.net.xml"
net = sumolib.net.readNet(NET_FILE)

valid_entry_edges = []
valid_core_edges = []

for edge in net.getEdges():

    if edge.isSpecial():
        continue

    lanes = edge.getLanes()
    if len(lanes) == 0:
        continue

    # Check if ANY lane allows passenger vehicles
    allows_passenger = False
    for lane in lanes:
        perms = lane.getPermissions()
        if perms is None or "passenger" in perms:
            allows_passenger = True
            break

    if not allows_passenger:
        continue

    # Entry edges: no incoming connections
    if len(edge.getIncoming()) == 0:
        valid_entry_edges.append(edge)

    # Core edges: high connectivity
    if len(edge.getIncoming()) > 2 and len(edge.getOutgoing()) > 2:
        valid_core_edges.append(edge)

print("Valid Entry Edge:", valid_entry_edges[0].getID())
print("Valid Core Edge:", valid_core_edges[0].getID())