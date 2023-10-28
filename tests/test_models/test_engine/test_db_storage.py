#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""
from datetime import datetime
import inspect
import models
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.engine import db_storage
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import unittest
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}
os.environ['HBNB_TYPE_STORAGE'] = 'db'

class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestDBStorage(unittest.TestCase):
    """Test the FileStorage class"""

    @classmethod
    def setUpClass(cls):
        """This will prepare the database to test db storage methods"""
        from models import storage
        cls.storage = storage

        cls.engine = cls.storage._DBStorage__engine

        cls.engine.execute(
                "CREATE DATABASE IF NOT EXISTS hbnb_test_db; ")
        cls.engine.execute(
                "CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost'"
                + " IDENTIFIED BY 'hbnb_test_pwd'; ")
        cls.engine.execute(
                "GRANT ALL PRIVILEGES ON 'hbnb_test_db'.* TO "
                + "'hbnb_test'@'localhost'; ")
        cls.engine.execute(
                "GRANT SELECT ON 'performance_schema'.* TO "
                + "'hbnb_test'@'localhost'; ")
        cls.engine.execute("FLUSH PRIVILEGES; ")
        HBNB_MYSQL_USER = 'hbnb_test'
        HBNB_MYSQL_PWD = 'hbnb_test_pwd'
        HBNB_MYSQL_HOST = 'localhost'
        HBNB_MYSQL_DB = 'hbnb_test_db'
        temp_engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                    format(HBNB_MYSQL_USER,
                                           HBNB_MYSQL_PWD,
                                           HBNB_MYSQL_HOST,
                                           HBNB_MYSQL_DB))
        cls.engine = temp_engine
        # Setup sessions and engine
        Base.metadata.create_all(cls.engine)
        sess_factory = sessionmaker(bind=cls.session, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        cls.session = Session

    @classmethod
    def tearDownClass(cls):
        """remove test components after running this test"""
        Base.metadata.drop_all(cls.engine)
        models.storage_t = 'file'

    def setUp(self):
        """setup a database"""
        os.putenv("HBNB_TYPE_STORAGE", "db")
        self.user1 = User(email='1chinonso@gmail.com', password='password')
        self.user2 = User(email='4chinonso@gmail.com', password='5password')
        self.user3 = User(email='3chinonso@gmail.com', password='6password')
        self.session.new(self.user1)
        self.session.new(self.user2)
        self.session.new(self.user3)
        self.session.save()

    def tearDown(self):
        """This will remove all changes created for testing purposes"""
        self.session.delete(self.user1)
        self.session.delete(self.user2)
        self.session.delete(self.user3)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage now")
    def test_get(self):
        """Test that get properly get the object base on id and class object"""
        self.assertIsNotNone(self.session.get(User, self.user1.id))
        self.assertIsNotNone(self.session.get(User, self.user2.id))
        self.assertIsNotNone(self.session.get(User, self.user3.id))

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage now")
    def test_count(self):
        """This will confirm if count method of storage counts correctly"""
        self.assertEqual(3, self.session.count(User))
        self.assertEqual(0, self.session.count(State))
        self.assertEqual(3, self.session.count())
