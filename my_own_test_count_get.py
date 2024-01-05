#!/usr/bin/python3
""" Test .get() and .count() methods
"""
from models import storage
from models.state import State
from models.user import User
from models.city import City
from models.place import Place
from models.review import Review
from models.amenity import Amenity

print("All objects: {}".format(storage.count()))
print("State objects: {}".format(storage.count(State)))
print("User objects: {}".format(storage.count(User)))
print("Place objects: {}".format(storage.count(Place)))
print("City objects: {}".format(storage.count(City)))
print("Amenity objects: {}".format(storage.count(Amenity)))
print("Review objects: {}".format(storage.count(Review)))


first_state_id = list(storage.all(State).values())[0].id
print("First state: {}".format(storage.get(State, first_state_id)))
