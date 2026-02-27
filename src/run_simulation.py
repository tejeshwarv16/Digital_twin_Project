# -*- coding: utf-8 -*-

import os
import csv
import random
import math
import traci

# =============================
# CONFIGURATION
# =============================

NET_FILE = "data/sumo_network/hinjewadi_phase3.net.xml"
ROUTE_FILE = "data/sumo_network/hinjewadi_peak.rou.xml"
SUMO_BINARY = "sumo"

SIMULATION_STEPS = 1800

# ---- Feature Toggles ----
ENABLE_AGGRESSION = True
ENABLE_CONTAGION = True
ENABLE_WRONG_WAY = True
ENABLE_SPEED_SURGE = True

# ---- Conservative Scaling ----
AGGRESSION_SCALE = 0.20

CONTAGION_RADIUS = 15.0
CONTAGION_DURATION = 4
CONTAGION_MULTIPLIER = 1.10

WRONG_WAY_PROB_SCALE = 0.005
WRONG_WAY_DURATION = 2

SURGE_MULTIPLIER = 1.05
SURGE_DURATION = 2
SURGE_COOLDOWN = 20
SURGE_PRESSURE_THRESHOLD = 1.3

# =============================
# START SUMO
# =============================

sumo_cmd = [
    SUMO_BINARY,
    "-n", NET_FILE,
    "-r", ROUTE_FILE,
    "--start",
    "--quit-on-end"
]

traci.start(sumo_cmd)

os.makedirs("data/logs", exist_ok=True)
log_file = open("data/logs/vehicle_log.csv", "w", newline="")
writer = csv.writer(log_file)

writer.writerow([
    "time", "vehicle_id", "x", "y",
    "speed", "waiting_time", "lane_id",
    "violation_type"
])

# =============================
# STATE STORAGE
# =============================

driver_traits = {}
vehicle_capability = {}
recent_violations = []
wrong_way_active = {}
surge_active = {}
surge_cooldown = {}

step = 0

# =============================
# SIMULATION LOOP
# =============================

while step < SIMULATION_STEPS:

    traci.simulationStep()
    vehicle_ids = traci.vehicle.getIDList()

    # Remove expired contagion
    recent_violations = [
        v for v in recent_violations
        if step - v["time"] <= CONTAGION_DURATION
    ]

    for vid in vehicle_ids:

        if vid not in driver_traits:
            driver_traits[vid] = random.random()
            vehicle_capability[vid] = 1.0 if "bike" in vid else 0.6
            surge_cooldown[vid] = 0

        x, y = traci.vehicle.getPosition(vid)
        speed = traci.vehicle.getSpeed(vid)
        waiting = traci.vehicle.getWaitingTime(vid)
        lane_id = traci.vehicle.getLaneID(vid)
        desired_speed = traci.vehicle.getMaxSpeed(vid)

        # =============================
        # PRESSURE MODEL
        # =============================

        pressure = min(waiting / 60.0, 1.0)

        if desired_speed > 0:
            pressure += max(0, desired_speed - speed) / desired_speed

        # Mild contagion boost
        if ENABLE_CONTAGION:
            for event in recent_violations:
                dist = math.hypot(x - event["x"], y - event["y"])
                if dist < CONTAGION_RADIUS:
                    pressure *= CONTAGION_MULTIPLIER
                    break

        # Cap pressure to prevent runaway
        pressure = min(pressure, 2.0)

        aggressiveness = driver_traits[vid]
        capability = vehicle_capability[vid]

        violation_type = "none"

        # =============================
        # AGGRESSIVE LANE CHANGE
        # =============================

        if ENABLE_AGGRESSION:
            violation_prob = aggressiveness * capability * pressure * AGGRESSION_SCALE

            if random.random() < violation_prob:
                try:
                    current_lane = traci.vehicle.getLaneIndex(vid)
                    edge_id = traci.vehicle.getRoadID(vid)
                    num_lanes = traci.edge.getLaneNumber(edge_id)

                    if num_lanes > 1:
                        if current_lane + 1 < num_lanes:
                            traci.vehicle.changeLane(vid, current_lane + 1, 3)
                        elif current_lane - 1 >= 0:
                            traci.vehicle.changeLane(vid, current_lane - 1, 3)

                        violation_type = "aggressive_lane_change"

                        recent_violations.append({
                            "time": step,
                            "x": x,
                            "y": y
                        })

                except:
                    pass

        # =============================
        # WRONG WAY (Rare, Multi-lane only)
        # =============================

        if ENABLE_WRONG_WAY:
            edge_id = traci.vehicle.getRoadID(vid)
            num_lanes = traci.edge.getLaneNumber(edge_id)

            if num_lanes > 1 and random.random() < aggressiveness * WRONG_WAY_PROB_SCALE:
                try:
                    route = traci.vehicle.getRoute(vid)

                    if len(route) > 1:
                        reversed_edge = "-" + route[0] if not route[0].startswith("-") else route[0][1:]
                        traci.vehicle.setRoute(vid, [reversed_edge] + route[1:])
                        wrong_way_active[vid] = step + WRONG_WAY_DURATION
                        violation_type = "wrong_way_short"

                        recent_violations.append({
                            "time": step,
                            "x": x,
                            "y": y
                        })

                except:
                    pass

        if vid in wrong_way_active and step > wrong_way_active[vid]:
            try:
                original_route = traci.vehicle.getRoute(vid)
                traci.vehicle.setRoute(vid, original_route)
            except:
                pass
            del wrong_way_active[vid]

        # =============================
        # SHORT SPEED SURGE (With cooldown)
        # =============================

        if ENABLE_SPEED_SURGE:

            if step >= surge_cooldown[vid] and pressure > SURGE_PRESSURE_THRESHOLD:
                if random.random() < aggressiveness * 0.1:

                    try:
                        traci.vehicle.setSpeed(vid, speed * SURGE_MULTIPLIER)
                        surge_active[vid] = step + SURGE_DURATION
                        surge_cooldown[vid] = step + SURGE_COOLDOWN
                        violation_type = "speed_surge"
                    except:
                        pass

        if vid in surge_active and step > surge_active[vid]:
            try:
                traci.vehicle.setSpeed(vid, -1)
            except:
                pass
            del surge_active[vid]

        # =============================
        # LOGGING
        # =============================

        writer.writerow([
            step, vid, x, y,
            speed, waiting, lane_id,
            violation_type
        ])

    step += 1

log_file.close()
traci.close()

print("[PASS] Conservative realism simulation completed.")