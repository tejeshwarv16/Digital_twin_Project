# -*- coding: utf-8 -*-


import sumolib

NET_FILE = "data/sumo_network/hinjewadi_phase3.net.xml"

net = sumolib.net.readNet(NET_FILE)

edge_id = "-1151423646#1"  # change if needed
edge = net.getEdge(edge_id)

print("Edge ID:", edge.getID())
print("Number of lanes:", len(edge.getLanes()))

for lane in edge.getLanes():
    print("Lane ID:", lane.getID())
    print("Permissions:", lane.getPermissions())