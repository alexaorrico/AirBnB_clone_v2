#!/usr/bin/python3
""" Test .get() and .count() methods
"""
from models import storage
from models.state import State

print("All objects: {}".format(storage.count()))
print("State objects: {}".format(storage.count(State)))

first_state_id = '0e391e25-dd3a-45f4-bce3-4d1dea83f3c7'
print("First state: {}".format(storage.get(State, first_state_id)))

