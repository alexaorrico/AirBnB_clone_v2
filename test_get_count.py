#!/usr/bin/python3
<<<<<<< HEAD

"""
Test .get() and .count() methods
=======
""" Test .get() and .count() methods
>>>>>>> bfcb10619fc065dc0acff513eb87a4eb63a3ac76
"""
from models import storage
from models.state import State

print("All objects: {}".format(storage.count()))
print("State objects: {}".format(storage.count(State)))

first_state_id = list(storage.all(State).values())[0].id
print("First state: {}".format(storage.get(State, first_state_id)))
