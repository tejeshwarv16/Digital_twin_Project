# Hinjewadi Digital Twin Project

**Behaviorally-Aware Urban Traffic Twin with Predictive World Modeling**

---

## 1. Project Overview

This project builds a **behaviorally-augmented Digital Twin of Hinjewadi Phase 3 (Pune, India)** using:

* OpenStreetMap (OSM)
* SUMO (Simulation of Urban Mobility)
* Python (OSMnx, TraCI)
* Structured lane-level logging
* Graph-based congestion modeling
* PyTorch (world model prototype)

The goal is not just traffic simulation.

The goal is to build a **structured, dynamic replica of a real urban region** that can:

* Model lawful traffic behavior
* Model probabilistic rule violations
* Analyze congestion propagation
* Learn predictive dynamics
* Serve as a foundation for defensive navigation research

This project treats traffic as a **complex adaptive system**, not a perfectly rule-compliant one.

---

# 2. What This Project Is

This is an **early-stage Digital Twin prototype** of Hinjewadi Phase 3.

It includes:

✔ Real road topology from OpenStreetMap
✔ Lane-level connectivity
✔ Traffic flow simulation
✔ Behavioral violation injection
✔ Structured state logging
✔ Congestion hotspot detection
✔ Temporal propagation analysis
✔ Lane-graph construction
✔ Predictive world modeling prototype

It is not just SUMO scripting.

It is a controlled experimental platform for studying:

* Traffic intelligence
* Adversarial micro-behavior
* Defensive navigation systems
* Propagation dynamics
* Learned world modeling

---

# 3. Why This Project Exists

Indian urban traffic does not follow idealized rules.

Real-world behavior includes:

* Aggressive lane changes
* Opportunistic overtaking
* Speed surges
* Pressure-induced deviations
* Congestion ripple effects

Autonomous navigation systems trained only in rule-perfect environments will fail under such conditions.

This project aims to:

1. Model lawful traffic.
2. Inject structured micro-violations.
3. Quantify congestion formation.
4. Analyze temporal and spatial propagation.
5. Build predictive lane-level world models.
6. Prepare for reinforcement-based navigation intelligence.

Traffic is treated as a **structured adversarial environment**.

---

# 4. System Architecture

The project operates in layered stages:

---

## Layer 1 — Topology Reconstruction

* Extract Hinjewadi Phase 3 from OSM
* Convert to SUMO network
* Preserve lanes, junctions, and connectivity
* Validate network integrity

Output:

```
data/raw_osm/
data/sumo_network/
```

---

## Layer 2 — Baseline Traffic Simulation

* Generate configurable traffic flows
* Simulate peak-hour congestion
* Log vehicle-level state at every timestep

Logged Features:

* Time
* Vehicle ID
* Position (x, y)
* Speed
* Waiting time
* Lane ID
* Violation type

Output:

```
data/logs/vehicle_log.csv
```

---

## Layer 3 — Behavioral Injection Engine

Each vehicle is assigned:

* Driver aggressiveness ∈ [0,1]
* Vehicle capability factor

Violations are probabilistic and pressure-triggered.

### Implemented Micro-Violations

* Aggressive lane change
* Speed surge under pressure

Future:

* Short wrong-way hops
* Risky merges
* Lane-blocking behavior

These create:

* Micro turbulence
* Local instability
* Realistic congestion ripple
* Defensive learning signals

---

## Layer 4 — Congestion Intelligence

Implemented analytics:

### Hotspot Analysis

* Average speed per lane
* Congestion ratio
* Violation ratio
* Correlation between violations and congestion

### Temporal Causality

* Lag correlation between violations and congestion
* Per-lane propagation timing

### Junction Propagation Analysis

* Congestion spread across junctions
* Delay propagation estimation
* Identified strongest negative propagation junctions

Results stored in:

```
results/
```

---

## Layer 5 — Structured World State Tensor

Built lane-level temporal dataset:

Features per lane per timestep:

* Mean speed
* Vehicle density
* Violation count
* Congestion state
* Future congestion label

Output:

```
data/processed/lane_time_tensor.csv
```

Statistics (current build):

* 157 active lanes
* 1790 timesteps
* ~3.4% future congestion rate

---

## Layer 6 — Lane Graph Construction

Constructed adjacency graph between active lanes using SUMO connectivity.

Output:

```
data/processed/lane_graph_edges.csv
```

Filtered graph:

* 157 lanes
* 164 connectivity edges
* 1 isolated lane

---

## Layer 7 — Predictive World Model Prototype

Trained PyTorch model to predict future congestion from:

* Lane-level features
* Connectivity graph

Current results:

* Accuracy ≈ 81%
* Precision ≈ 0.20
* Recall ≈ 0.95
* F1 ≈ 0.33

Interpretation:

The model strongly detects congestion (high recall),
but over-predicts (low precision).

This is expected under class imbalance and early-stage modeling.

---

# 5. Project Structure

```
Digital_twin_Project/
│
├── src/
│   ├── test.py
│   ├── extract_hinjewadi.py
│   ├── build_lane_graph.py
│   ├── run_simulation.py
│   ├── analyze_hotspots.py
│   ├── lane_temporal_analysis.py
│   ├── junction_propagation_analysis.py
│   ├── build_world_state_tensor.py
│   ├── train_world_model.py
│
├── data/
│   ├── raw_osm/
│   ├── sumo_network/
│   ├── logs/
│   ├── processed/
│
├── results/
│
├── requirements.txt
└── README.md
```

---

# 6. Installation Guide

## 1. Clone Repository

```
git clone git@github.com:tejeshwarv16/Digital_twin_Project.git
cd Digital_twin_Project
```

---

## 2. Create Conda Environment

```
conda create -n hinjewadi_twin python=3.10
conda activate hinjewadi_twin
```

---

## 3. Install Python Dependencies

```
pip install -r requirements.txt
```

If missing:

```
pip install osmnx networkx matplotlib pandas numpy torch
```

---

## 4. Install SUMO

Download:
[https://www.eclipse.org/sumo/](https://www.eclipse.org/sumo/)

Verify:

```
sumo --version
```

---

## 5. Verify Setup

```
python src/test.py
```

All dependencies should pass.

---

# 7. Current Milestones

### Milestone 1 — Environment Setup

✔ Python environment
✔ SUMO integration
✔ TraCI working
✔ Git configured

### Milestone 2 — Network Construction

✔ OSM extraction
✔ SUMO network conversion
✔ Network validation

### Milestone 3 — Simulation + Logging

✔ Traffic flow generation
✔ Behavioral injection
✔ Structured CSV logging

### Milestone 4 — Congestion Intelligence

✔ Hotspot detection
✔ Temporal causality
✔ Junction propagation analysis

### Milestone 5 — World Modeling

✔ Lane-time tensor construction
✔ Lane graph extraction
✔ Predictive congestion model

---

# 8. Research Direction

Short-Term:

* Improve world model precision
* Address class imbalance
* Implement ego navigation agent
* Begin reinforcement-based decision learning

Mid-Term:

* Model-based RL using learned transition dynamics
* Defensive navigation policy training
* Rare-event stress testing

Long-Term:

* Structured world foundation model
* Generalizable urban traffic intelligence
* Causal dynamic systems learning under adversarial conditions

---

# 9. Current Status Summary

This project is:

A behaviorally-augmented digital twin prototype
with predictive congestion modeling
and lane-level propagation analysis.

It is not yet calibrated against real traffic data.

It is a research platform for building intelligent navigation systems under uncertainty.

---
