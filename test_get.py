#!/usr/bin/python3
""" Test .get()
"""
from models import storage
from models.state import State

state = storage.get(State, "Doesn't exist")
if state is None:
    print("None", end="")
else:
    print("Get shouldn't return an object if the ID doesn't exist", end="")
