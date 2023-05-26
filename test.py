from models.base_model import BaseModel
from models import storage
from models.city import City
from models.engine.file_storage import FileStorage
from models.state import State

# storage.reload()
# obj_dict = storage.all(State)
# print(obj_dict)
# id_ = 'State.742b36a2-f1dc-4d5e-9fc7-6723f81f19da'
# print(obj_dict[id_])
print(storage.count(City))


