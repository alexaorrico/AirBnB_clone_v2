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
state1 = State()
state2 = State()
city1 = City()
user1 = User()

storage.add(state1)
storage.add(state2)
storage.add(city1)
storage.add(user1)
storage.save()

objs = storage.all()
print(objs)