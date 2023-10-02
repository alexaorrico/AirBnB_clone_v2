#!/usr/bin/python3
from models.base_model import BaseModel

my_model = BaseModel(['city_id="0001"',
                      'user_id="0001"',
                      'name="My_little_house"',
                      'number_rooms=4',
                      'number_bathrooms=2',
                      'max_guest=10',
                      'price_by_night=300',
                      'latitude=37.773972',
                      'longitude=-122.431297'])
"""
print(my_model)
print('\n\n\n')
my_model.save()
print(my_model)
print('\n\n\n')
my_model_json = my_model.to_json()
print(my_model_json)
print('\n\n\n')
print("JSON of my_model:")
print('\n\n\n')
for key in my_model_json.keys():
    print("\t{}: ({}) - {}".format(key, type(my_model_json[key]),
                                   my_model_json[key]))
"""
