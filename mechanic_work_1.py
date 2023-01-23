#!/usr/bin/python3
'''Mechanic Work 1'''
from models.state import State
from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage
from models.amenity import Amenity


# house_db = FileStorage()
house_db = DBStorage()
for _ in range(5):
    house_1 = Amenity()
    house_db.new(house_1)
    house_db.save()

for _ in range(5):
    house_1 = State()
    house_db.new(house_1)
    house_db.save()
