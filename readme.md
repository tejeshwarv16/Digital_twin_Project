# Hinjewadi Digital Twin Project

## Overview

This project builds a **behaviorally-aware Digital Twin of Hinjewadi Phase 3 (Pune, India)** using:

* OpenStreetMap (OSM)
* SUMO (Simulation of Urban Mobility)
* Python (OSMnx, TraCI)
* Structured behavioral modeling
* Future PyTorch-based predictive systems

The system reconstructs real urban topology and simulates traffic flow under both lawful and probabilistic rule-deviating agents.

This is not just a traffic simulator.

It is a controlled experimental environment for studying:

* Congestion dynamics
* Micro-violations and system fragility
* Defensive navigation modeling
* Structured adversarial environments
* Foundations for future world models

---

# What This Project Is

This is a **Digital Twin** of a real urban region.

The twin:

* Extracts real road topology from OpenStreetMap
* Converts it into a SUMO simulation network
* Simulates traffic demand and congestion buildup
* Injects probabilistic, pressure-driven driver deviations
* Logs full vehicle state evolution for analysis

The goal is to transform a static road network into a measurable, dynamic behavioral system.

---

# Why This Project Exists

Indian urban traffic is not rule-perfect.

Real-world traffic includes:

* Unsignaled lane changes
* Opportunistic overtaking
* Pressure-induced aggressive behavior
* Rare wrong-way maneuvers
* Adaptive local responses

Autonomous navigation systems that assume perfect rule compliance will underperform in such environments.

This project aims to:

1. Model lawful traffic dynamics.
2. Introduce controlled micro-violations.
3. Measure how local deviations affect system-level congestion.
4. Quantify fragility under behavioral noise.
5. Generate structured datasets for robust navigation modeling.

Traffic is treated as a structured, partially adversarial system — not a deterministic one.

---

# System Architecture

The Digital Twin operates in layered form.

---

## Layer 1 — Real Topology Reconstruction

* Road network extracted using OSMnx
* Converted into SUMO-compatible format
* Lanes, junctions, connectivity preserved

This layer provides structural realism.

---

## Layer 2 — Baseline Traffic Flow

* Configurable traffic demand
* Peak-hour congestion buildup
* Full vehicle state logging
* Travel-time and bottleneck analysis

This establishes lawful baseline behavior.

---

## Layer 3 — Conservative Behavioral Engine

Vehicles are assigned:

* Driver aggressiveness ∈ [0,1]
* Vehicle capability factor (bike vs car)

At runtime, deviations are triggered probabilistically based on:

* Waiting time
* Speed deficit
* Local congestion pressure
* Nearby violation contagion

All behaviors are:

* State-triggered
* Probability-scaled
* Temporally bounded
* Damped to prevent runaway collapse

---

## Behavioral Rules (Conservative Realism Mode)

### Lawful Behavior

* Lane following
* Route adherence
* Speed constraints
* Signal compliance

---

### Probabilistic Micro-Violations

These are frequent but low-impact.

#### 1. Aggressive Lane Change

Triggered when:

* Speed deficit high
* Waiting time rising
* Adjacent lane available

Primary turbulence mechanism.

---

#### 2. Opportunistic Speed Surge

Short, rare burst:

* Activated under sustained pressure
* Cooldown enforced
* Duration limited
* No continuous amplification

Models uninformed overtaking behavior.

---

#### 3. Behavioral Contagion

* Nearby violations temporarily amplify pressure
* Local ripple effects only
* Strict time and radius bounds

Models frustration propagation.

---

#### 4. Short Wrong-Way Hop (Experimental)

* Extremely rare
* Only on multi-lane roads
* Duration capped
* No persistent route corruption

Used for controlled topology shock testing.

---

All violations are logged explicitly in the dataset.

---

## Layer 4 — Structured Logging

Each simulation logs per timestep:

* Timestamp
* Vehicle ID
* Position (x, y)
* Speed
* Waiting time
* Lane ID
* Violation type

This produces a behavior-labeled traffic dataset for:

* Congestion modeling
* Violation clustering analysis
* Predictive modeling
* Defensive navigation training

---

# Current Status

## Milestone 1 — Environment Setup

* Python environment configured
* SUMO installation verified
* TraCI integration working
* Dependency validation script implemented
* Git version control configured

---

## Milestone 2 — Network Construction

* Hinjewadi Phase 3 extracted from OSM
* Converted to SUMO network
* Network validated
* Baseline lawful simulation executed

---

## Milestone 3 — Congestion Analysis

* Vehicle-level CSV logging implemented
* Congestion lifecycle analyzed
* Peak congestion timing measured
* Baseline vs deviation comparisons performed

---

## Milestone 4 — Conservative Behavioral Engine (Stable)

* Aggressive lane-change modeling
* Bounded speed surge mechanism
* Contagion effect implemented
* Violation damping added
* Stable 1800-step simulations validated

System exhibits:

* ~2–5% deviation rate
* Increased congestion without collapse
* Late-stage peak saturation
* No runaway instability

---

# Project Structure

```
Digital_twin_Project/
│
├── src/
│   ├── test.py
│   ├── extract_hinjewadi.py
│   ├── generate_flows.py
│   ├── select_zones.py
│   ├── run_simulation.py
│
├── data/
│   ├── raw_osm/
│   ├── sumo_network/
│   ├── logs/
│
├── results/
│
├── requirements.txt
└── README.md
```

---

# Installation Guide

## 1. Clone Repository

```bash
git clone git@github.com:tejeshwarv16/Digital_twin_Project.git
cd Digital_twin_Project
```

---

## 2. Create Conda Environment

```bash
conda create -n hinjewadi_twin python=3.10
conda activate hinjewadi_twin
```

---

## 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

If needed:

```bash
pip install osmnx networkx matplotlib pandas numpy torch
```

---

## 4. Install SUMO

Download from:

[https://www.eclipse.org/sumo/](https://www.eclipse.org/sumo/)

Verify:

```bash
sumo --version
```

---

## 5. Verify Environment

```bash
python src/test.py
```

Expected output:

```
[PASS] Import osmnx
[PASS] Import networkx
[PASS] SUMO binary accessible
[PASS] TraCI import
```

---

# Research Direction

## Short-Term

* Spatial violation clustering analysis
* Congestion hotspot correlation
* Lawful vs behavioral comparison metrics
* Travel-time inflation quantification

## Mid-Term

* Predictive congestion modeling
* Deviation probability learning
* Defensive navigation strategy evaluation

## Long-Term Vision

Use structured traffic systems as a foundation for:

* Robust world modeling
* Causal dynamic system learning
* Autonomous navigation under uncertainty
* Behavior-aware simulation environments

---

# Author

Tejeshwar V
AI Research & Autonomous Systems

---