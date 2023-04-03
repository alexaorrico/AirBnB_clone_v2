#!/usr/bin/python3
""" Test .get() and .count() methods
"""
from models import storage
from models.state import State

# get the count for all the objects in the db
print("All objects: {}".format(storage.count()))
# get the count for all the  states in the db
print("State objects: {}".format(storage.count(State)))

first_state_id = list(storage.all(State).values())[0].id
# print the first state object using get method
print("First state: {}".format(storage.get(State, first_state_id)))