#!/usr/bin/python3
from models import storage
from models.state import State
f_id = list(storage.all(State).values())[0].id
obj = storage.get(State, f_id)
number = storage.count(State)
print(obj)
print(number)
