import unittest
import inspect
import models
from models import storage
from models.user import User
from models.engine.db_storage import DBStorage
from models.state import State
import pycodestyle
from models.base_model import BaseModel, Base
import os
import MySQLdb
from os import getenv

# set the env variables
storage_t = os.getenv("HBNB_TYPE_STORAGE")
class TestDBStorage(unittest.TestCase):
    """Test documentation and style."""

    @classmethod
    def setUpClass(cls):
        """Set up the test environment"""        
        if type(models.storage) == DBStorage:
            db = MySQLdb.connect(user=os.getenv("HBNB_MYSQL_USER"),
                                 passwd=os.getenv("HBNB_MYSQL_PWD"),
                                 db=os.getenv("HBNB_MYSQL_DB"))
            cls.cursor = db.cursor()
            cls.storage = DBStorage()
            cls.storage.reload()
            cls.state = State(name="Marwa")
            cls.user = User(email="marwa@mydomain.com",
                            password="password")
            cls.storage._DBStorage__session.add(cls.state)
            cls.storage._DBStorage__session.add(cls.user)
            cls.storage._DBStorage__session.commit()
    
    def new(self, obj):
        """Add the object to the current database session."""
        self.storage.new(obj)
    
    @classmethod
    def tearDown(self):
        if type(models.storage) == DBStorage:
            cls.cursor.close()
            cls.storage._DBStorage__session.close()

    def dtest_all(self):
        """Test the all() method"""
        obj_dict = self.storage.all()
        self.assertIsInstance(obj_dict, dict)
        self.assertGreaterEqual(len(obj_dict), 0) 

    @unittest.skipIf(models.storage_t != "db", "not testing file storage")
    def test_new(self):
        """Testing new method."""
        ny = State(name="New York")
        self.storage.new(ny)
        self.assertIn(ny, list(self.storage._DBStorage__session.new))
        self.storage._DBStorage__session.rollback()
    

    @unittest.skipIf(models.storage_t != "db", "not testing file storage")
    def test_get(self):
        """Testing get method."""
        self.assertEqual(self.storage.get("User", self.user.id), self.user)
 
    def dtest_get(self):
        state = State(name="New York4")
        self.storage.new(state)
        self.storage.save()
        
        result = self.storage.all(State).values()
        self.assertEqual(state, list(result)[0])

    def dtest_count(self):
        state1 = State(name="New York")
        state2 = State(name="New York2")
        self.storage.new(state1)
        self.storage.new(state2)
        self.storage.save()

        count = self.storage.count(State)
        self.assertEqual(count, 2)

    def dtest_pep8_conformance(self):
        """ this is test pycodestyle"""
        style = pycodestyle.StyleGuide()
        result = style.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0)


if __name__ == '__main__':
    unittest.main()

