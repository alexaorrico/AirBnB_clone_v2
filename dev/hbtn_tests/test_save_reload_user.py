#!/usr/bin/python3
from models import storage
from models.base_model import BaseModel
from models.user import User

all_objs = storage.all()
print("-- End Reloaded objects --")
print("printing values only of reloaded:")
for obj_id in all_objs.keys():
    obj = all_objs[obj_id]
    print(obj)

print("-- Begin Create a new User --")
my_user = User()
my_user.first_name = "Betty"
my_user.last_name = "Holberton"
my_user.email = "airbnb@holbertonshool.com"
my_user.password = "root"
my_user.save()
an_bm = BaseModel()
an_bm.save()
print(my_user)
