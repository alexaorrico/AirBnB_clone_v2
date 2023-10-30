#!/usr/bin/python3

from models import storage, storage_t
from models.user import User
from models.state import State
from models.city import City

print(storage_t)



# __storage = FileStorage()
# _class = classes["BaseModel"]
# id = "6ce60608-5137-4b80-bc45-ea6320ecc669"
# data = __storage.get(_class, id)
# counts = __storage.count(_class)
# print(data)
# print(counts)

# TESTING DB
state1 = State(name="Abuja")
state2 = State(name="Lagos")
state3 = State(name="Abia")
state4 = State(name="Jos")
city1 = City(name="Life Camp", state_id=state1.id)
city2 = City(name="Platue", state_id=state4.id)


storage.new(state1)
storage.new(state2)
storage.new(city1)

storage.save()

objs = storage.all()
print(objs)