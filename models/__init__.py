#!/usr/bin/python3
"""
initialize the models package
"""

import os


storage_t = os.getenv("HBNB_TYPE_STORAGE")


if storage_t == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
storage.reload()
