#!/usr/bin/python3
""" Test .get() and .count() methods
"""
from models import storage
from models.state import State

print("All objects: {}".format(storage.count()))
print("State objects: {}".format(storage.count(State)))

first_state_id = "b5fc9076-6c20-44a7-ac9b-97de17112329"
print("First state: {}".format(storage.get(State, first_state_id)))
