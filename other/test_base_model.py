#!/usr/bin/python3
import sys
import os
sys.path.insert(1, os.path.join(os.path.split(__file__)[0], '..'))
# print(os.listdir())
# print(sys.path)
from models.base_model import BaseModel

my_model = BaseModel()
my_model.name = "Holberton"
my_model.my_number = 89
print(my_model.__dict__)
print(my_model)
my_model.save()
print(my_model)
my_model_json = my_model.to_json()
print(my_model_json)
print("JSON of my_model:")
for key in my_model_json.keys():
    print("\t{}: ({}) - {}".format(key, type
                                   (my_model_json[key]), my_model_json[key]))
