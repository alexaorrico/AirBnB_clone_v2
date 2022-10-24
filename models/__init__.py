import os
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

"""Classes - dictionary = { Class Name (string) : Class Type }"""

if os.environ.get('HBNB_TYPE_STORAGE') == 'db':
    from models.engine import db_storage
    Classes = db_storage.DBStorage.Classes
    storage = db_storage.DBStorage()
else:
    from models.engine import file_storage
    Classes = file_storage.FileStorage.Classes
    storage = file_storage.FileStorage()

storage.reload()
