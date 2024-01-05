#!/usr/bin/python3
"""document document"""

from models.engine.db_storage import DBStorage
import os
import unittest


@unittest.skipIf(
    os.getenv("HBNB_TYPE_STORAGE") != "db",
    "Test is not relevant for DBStorage"
)
class test_DB_Storage(unittest.TestCase):
    """document document"""

    def test_documentation(self):
        """document document"""
        self.assertIsNot(DBStorage.__doc__, None)
