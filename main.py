# -*- coding: utf-8 -*-
"""
Created on Fri Feb 27 23:47:43 2026

@author: tejes
"""

import os
import sys

SUMO_HOME = r"C:\Program Files (x86)\Eclipse\Sumo"
tools_path = os.path.join(SUMO_HOME, "tools")

sys.path.append(tools_path)

import traci

print("TraCI imported successfully.")