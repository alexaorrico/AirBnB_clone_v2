#!/usr/bin/python3
"""
initialize the models package
"""

from models.engine.file_storage import FileStorage

storage = FileStorage()
storage.reload()
