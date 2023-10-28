#!/usr/bin/python3
""" this script for Test .get() and .count() methods
"""
from models import storage
from models.state import State

print("All objects: {}".format(storage.count()))
print("State objects: {}".format(storage.count(State)))

first_state_id = list(storage.all(State))[0].id
print("First state: {}".format(storage.get(State, first_state_id)))
