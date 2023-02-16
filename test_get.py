#!/usr/bin/python3
""" Test .get() and .count() methods
"""
from models import storage
from models.state import State

<<<<<<< HEAD
first_state_id = list(storage.all(State).values())[0].id 
=======

print("All objects: {}".format(storage.count()))
print("State objects: {}".format(storage.count(State)))
first_state_id = list(storage.all(State).values())[0].id

>>>>>>> DBStorage
print(first_state_id)
print("First state: {}".format(storage.get(State, first_state_id)))
