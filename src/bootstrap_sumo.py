# -*- coding: utf-8 -*-
"""
Created on Fri Feb 27 23:46:58 2026

@author: tejes
"""

import os
import sys

SUMO_HOME = r"C:\Program Files (x86)\Eclipse\Sumo"

if not os.path.exists(SUMO_HOME):
    raise EnvironmentError("SUMO_HOME path is incorrect")

os.environ["SUMO_HOME"] = SUMO_HOME

tools_path = os.path.join(SUMO_HOME, "tools")

if tools_path not in sys.path:
    sys.path.append(tools_path)

print("SUMO tools path added successfully.")