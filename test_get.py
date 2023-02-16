#!/usr/bin/python3
""" Test .get() and .count() methods
"""
from models import storage
from models.city import City

print("All objects: {}".format(storage.count()))
print("State objects: {}".format(storage.count(City)))

first_City_id = list(storage.all(City).values())[0].id
print("First City: {}".format(storage.get(City, first_City_id)))
