# -*- coding: utf-8 -*-
"""
Created on Fri Feb 27 23:52:49 2026

@author: tejes
"""

"""
Environment & Dependency Test Script
Hinjewadi Digital Twin Project
"""

import os
import sys
import subprocess
import importlib


def print_status(name, success, error=None):
    if success:
        print(f"[PASS] {name}")
    else:
        print(f"[FAIL] {name}")
        if error:
            print(f"       -> {error}")


def test_python_packages():
    packages = ["osmnx", "networkx", "matplotlib", "pandas", "numpy", "torch"]
    for pkg in packages:
        try:
            importlib.import_module(pkg)
            print_status(f"Import {pkg}", True)
        except Exception as e:
            print_status(f"Import {pkg}", False, e)


def test_sumo_binary():
    try:
        result = subprocess.run(["sumo", "--version"],
                                capture_output=True,
                                text=True)
        if result.returncode == 0:
            print_status("SUMO binary accessible", True)
        else:
            print_status("SUMO binary accessible", False, result.stderr)
    except Exception as e:
        print_status("SUMO binary accessible", False, e)


def test_sumo_gui():
    try:
        result = subprocess.run(["sumo-gui", "--version"],
                                capture_output=True,
                                text=True)
        if result.returncode == 0:
            print_status("SUMO GUI accessible", True)
        else:
            print_status("SUMO GUI accessible", False, result.stderr)
    except Exception as e:
        print_status("SUMO GUI accessible", False, e)


def test_traci():
    try:
        SUMO_HOME = r"C:\Program Files (x86)\Eclipse\Sumo"
        tools_path = os.path.join(SUMO_HOME, "tools")

        if tools_path not in sys.path:
            sys.path.append(tools_path)

        import traci
        print_status("TraCI import", True)
    except Exception as e:
        print_status("TraCI import", False, e)


if __name__ == "__main__":
    print("\n=== Hinjewadi Digital Twin Environment Test ===\n")

    test_python_packages()
    test_sumo_binary()
    test_sumo_gui()
    test_traci()

    print("\n=== Test Complete ===\n")