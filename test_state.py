#!/usr/bin/python3
from models.state import State
from models.engine.db_storage import DBStorage

storage = DBStorage()
storage.reload()

new_state = State(name="California")
storage.new(new_state)
storage.save()
