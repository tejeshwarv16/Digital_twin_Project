# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import os


def create_peak_flow(route_path):

    routes = ET.Element("routes")

    ET.SubElement(routes, "vType", {
        "id": "car",
        "accel": "2.6",
        "decel": "4.5",
        "length": "5",
        "maxSpeed": "16",
        "sigma": "0.5"
    })

    ET.SubElement(routes, "vType", {
        "id": "bike",
        "accel": "3.5",
        "decel": "5.0",
        "length": "2",
        "maxSpeed": "18",
        "sigma": "0.7"
    })

    ENTRY_EDGE = "239840578#0"
    CORE_EDGE = "-1030313018#1"

    ET.SubElement(routes, "flow", {
        "id": "morning_cars",
        "type": "car",
        "begin": "0",
        "end": "3600",
        "vehsPerHour": "900",
        "from": ENTRY_EDGE,
        "to": CORE_EDGE
    })

    ET.SubElement(routes, "flow", {
        "id": "morning_bikes",
        "type": "bike",
        "begin": "0",
        "end": "3600",
        "vehsPerHour": "1200",
        "from": ENTRY_EDGE,
        "to": CORE_EDGE
    })

    tree = ET.ElementTree(routes)
    tree.write(route_path)
    print(f"[PASS] Route file created at {route_path}")


if __name__ == "__main__":
    os.makedirs("data/sumo_network", exist_ok=True)
    create_peak_flow("data/sumo_network/hinjewadi_peak.rou.xml")