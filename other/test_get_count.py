#!/usr/bin/python3
""" Test .get() and .count() methods
"""
import os
import sys
sys.path.insert(1, os.path.join(os.path.split(__file__)[0], '..'))
from models import storage

print("All objects: {}".format(storage.count()))
print("State objects: {}".format(storage.count("State")))

first_state_id = list(storage.all("State").keys())[0]
print("First state: {}".format(storage.get("State", first_state_id)))

print("Bad state: {}".format(storage.get("State", "-34643")))
