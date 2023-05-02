#!/usr/bin/python3
""" Test .get() and .count() methods
"""
from models.state import State
from models import storage

print("All objects: {}".format(storage.count()))
print("State objects: {}".format(storage.count(State)))

first_state_id = list(storage.all(State).values())[0].id
print("First state: {}".format(storage.get(State, first_state_id)))
