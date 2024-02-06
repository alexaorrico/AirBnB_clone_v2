#!/usr/bin/python3
""" Test .get() and .count() methods
"""
from models import storage
from models.state import State

print("All objects: {}".format(storage.count()))
print("State objects: {}".format(storage.count(State)))

all_states = list(storage.all(State).values())

if all_states:
    first_state_id = all_states[0].id
    print("First state: {}".format(storage.get(State, first_state_id)))
else:
    print("No State found yet")
