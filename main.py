#!/usr/bin/python3
""" Test .get() and .count() methods
"""
from models import storage
from models.state import State
from models.amenity import Amenity

print("All objects: {}".format(storage.count()))
print("State objects: {}".format(storage.count(State)))
print("Amenity objects: {}".format(storage.count(Amenity)))
