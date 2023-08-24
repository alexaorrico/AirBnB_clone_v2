#!/usr/bin/python3
import json
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

json_file_path = '/home/sunny/holbertonschool-AirBnB_clone_v3/file.json'

with open(json_file_path, 'r') as json_file:
    data = json.load(json_file)

for item_key, item_data in data.items():
    class_name, item_id = item_key.split('.')
    if class_name == "Amenity":
        obj = Amenity(**item_data)
    elif class_name == "BaseModel":
        obj = BaseModel(**item_data)
    elif class_name == "City":
        obj = City(**item_data)
    elif class_name == "Place":
        obj = Place(**item_data)
    elif class_name == "Review":
        obj = Review(**item_data)
    elif class_name == "State":
        obj = State(**item_data)
    elif class_name == "User":
        obj = User(**item_data)
    else:
        print(f"Unknown class: {class_name}")
        continue

    storage.new(obj)
    print("Added object:", obj)

storage.save()
print("Total objects in session:", len(storage.all()))
