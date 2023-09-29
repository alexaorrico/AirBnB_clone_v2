#!/usr/bin/python3
""" Test .get() and .count() methods
"""
from models import storage
from models.state import State

print("All objects: {}".format(storage.count()))
print("State objects: {}".format(storage.count(State)))

# Check if any State objects exist before trying to access the first one
state_objects = storage.all(State)
if state_objects:
    first_state_id = list(state_objects.values())[0].id
    print("First state: {}".format(storage.get(State, first_state_id)))
else:
    print("No State objects found.")

