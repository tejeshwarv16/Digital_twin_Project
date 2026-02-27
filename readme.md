# Hinjewadi Digital Twin Project

## Overview

This project aims to build a predictive Digital Twin of Hinjewadi Phase 3 (Pune, India) using:

- OpenStreetMap (OSM)
- SUMO (Simulation of Urban Mobility)
- Python (OSMnx, TraCI)
- PyTorch (future world model integration)

The goal is to simulate real-world traffic dynamics and later integrate a learned world model for predictive navigation.

---

## Current Status (Milestone 1)

✅ Python environment configured  
✅ SUMO installation verified  
✅ TraCI integration working  
✅ Dependency validation test script implemented  
✅ Git version control configured  

---

## Project Structure

```

Digital_twin_Project/
│
├── src/
│   ├── test.py
│   └── bootstrap_sumo.py
│
├── data/
├── results/
├── requirements.txt
└── README.md

````

---

## Installation Guide

### 1. Clone Repository

```bash
git clone git@github.com:tejeshwarv16/Digital_twin_Project.git
cd Digital_twin_Project
````

---

### 2. Create Conda Environment

```bash
conda create -n hinjewadi_twin python=3.10
conda activate hinjewadi_twin
```

---

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

If requirements.txt is not available:

```bash
pip install osmnx networkx matplotlib pandas numpy torch
```

---

### 4. Install SUMO

Download from:

[https://www.eclipse.org/sumo/](https://www.eclipse.org/sumo/)

After installation, ensure:

```bash
sumo --version
```

returns version information.

---

### 5. Verify Environment

Run:

```bash
python src/test.py
```

Expected output:

```
[PASS] Import osmnx
[PASS] Import networkx
...
[PASS] TraCI import
```

---

## Next Development Milestones

* Extract Hinjewadi Phase 3 road network
* Convert OSM to SUMO network
* Generate traffic flows
* Integrate predictive world model

---

## Author

Tejeshwar V
AI Research & Autonomous Systems Enthusiast

````

---

# Commit This README

```bash
git add README.md
git commit -m "Added project README with setup instructions and milestone 1 documentation"
git push
````
