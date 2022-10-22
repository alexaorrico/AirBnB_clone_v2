#!/usr/bin/python3
from models import storage
from models.state import State
from models.city import City
#f_id = State(name="Malawi")
#obj = storage.get(State, f_id.id)
#number = storage.count(State)
#print(obj)
print(storage.all(State))
#print(number)
