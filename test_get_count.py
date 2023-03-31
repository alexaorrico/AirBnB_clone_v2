#!/usr/bin/python3
from models import storage
from models.state import State
from models.city import City

all_objects_count = storage.count()
state_objects_count = storage.count(State)

print("All objects: {}".format(all_objects_count))
print("State objects: {}".format(state_objects_count))

states = storage.all(State)
print("States: {}".format(states))

first_state_id = list(states.values())[0].id
city_objects_count = storage.count(City, first_state_id)

print("City objects for the first state: {}".format(city_objects_count))
