#!/usr/bin/python3

from models import storage
from models.state import State

my_obj = State()
storage.get(my_obj, my_obj.id)
