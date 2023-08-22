#!/usr/bin/python3
""" Test .get() and .count() methods
"""
from models import storage
from models.city import City
from models.state import State

state1 = State(name="California")
state2 = State(name="New York")
city1 = City(name="San Francisco")

storage.new(state1)
storage.new(state2)
storage.new(city1)

print("All objects: {}".format(storage.count()))
print("State objects: {}".format(storage.count(State)))

first_state_id = list(storage.all(State).values())[0].id
print("First state: {}".format(storage.get(State, first_state_id)))
