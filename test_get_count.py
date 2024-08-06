#!/usr/bin/python3

"""
test .get() and .count() methods
"""

from  models import storage
from models.state import State

print("All objects: {}".format(storage.count()))
print("State objects: {}".format(storage.count(State)))

first_state_id = list(storage.all(State).values())[4].id
print("First State: {}".format(storage.get(State, first_state_id)))
