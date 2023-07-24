#!/usr/bin/python3
import subprocess
""" This file is intended to help debug task 5 """

c_ps = subprocess.Popen(['cat', 'drop_dev_database.sql'], stdout=subprocess.PIPE)
c_out = subprocess.check_output(['mysql', '-uroot', '-p'], stdin=c_ps.stdout)
c_ps.wait()
d_ps = subprocess.Popen(['cat', 'create_dev_database.sql'], stdout=subprocess.PIPE)
d_out = subprocess.check_output(['mysql', '-uroot', '-p'], stdin=d_ps.stdout)
d_ps.wait()

import models
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage

a = {}
s = {}
for i in range(10):
    a[f"a{i}"] = Amenity(name=f"amenity{i}")
    a[f"a{i}"].save()
    s[f"s{i}"] = State(name=f"state{i}")
    s[f"s{i}"].save()


# c_ps = subprocess.Popen(['cat', 'drop_dev_database.sql'], stdout=subprocess.PIPE)
# c_out = subprocess.check_output(['mysql', '-uroot', '-p'], stdin=c_ps.stdout)
# c_ps.wait()
