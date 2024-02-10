#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


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


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
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
import unittest
from unittest.mock import patch
from models.engine.db_storage import DBStorage
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class TestDBStorage(unittest.TestCase):
    """Tests for DBStorage class"""

    @classmethod
    def setUpClass(cls):
        """Set up the test environment"""
        cls.storage = DBStorage()

    def test_all(self):
        """Test the all method"""
        with patch('models.engine.db_storage.DBStorage.__session') as mock_session:
            mock_session.query.return_value.all.return_value = [
                Amenity(), City(), Place()
            ]
            result = self.storage.all()
            self.assertEqual(len(result), 3)
            self.assertIsInstance(result['Amenity.'], Amenity)
            self.assertIsInstance(result['City.'], City)
            self.assertIsInstance(result['Place.'], Place)

    def test_new(self):
        """Test the new method"""
        with patch('models.engine.db_storage.DBStorage.__session') as mock_session:
            obj = BaseModel()
            self.storage.new(obj)
            mock_session.add.assert_called_once_with(obj)

    def test_save(self):
        """Test the save method"""
        with patch('models.engine.db_storage.DBStorage.__session') as mock_session:
            self.storage.save()
            mock_session.commit.assert_called_once()

    def test_delete(self):
        """Test the delete method"""
        with patch('models.engine.db_storage.DBStorage.__session') as mock_session:
            obj = BaseModel()
            self.storage.delete(obj)
            mock_session.delete.assert_called_once_with(obj)

    def test_reload(self):
        """Test the reload method"""
        with patch('models.engine.db_storage.Base.metadata') as mock_metadata, \
                patch('models.engine.db_storage.sessionmaker') as mock_sessionmaker, \
                patch('models.engine.db_storage.scoped_session') as mock_scoped_session:
            self.storage.reload()
            mock_metadata.create_all.assert_called_once_with(self.storage._DBStorage__engine)
            mock_sessionmaker.assert_called_once_with(bind=self.storage._DBStorage__engine, expire_on_commit=False)
            mock_scoped_session.assert_called_once_with(mock_sessionmaker.return_value)
            self.assertEqual(self.storage._DBStorage__session, mock_scoped_session.return_value)

    def test_close(self):
        """Test the close method"""
        with patch('models.engine.db_storage.DBStorage.__session') as mock_session:
            self.storage.close()
            mock_session.remove.assert_called_once()

    def test_get(self):
        """Test the get method"""
        with patch('models.engine.db_storage.DBStorage.__session') as mock_session:
            cls = BaseModel
            id = "123"
            result = self.storage.get(cls, id)
            mock_session.query.assert_called_once_with(cls)
            mock_session.query.return_value.filter.assert_called_once_with(cls.id == id)
            mock_session.query.return_value.filter.return_value.first.assert_called_once()

    def test_count(self):
        """Test the count method"""
        with patch('models.engine.db_storage.DBStorage.all') as mock_all:
            cls = BaseModel
            mock_all.return_value = {
                'Amenity.1': Amenity(),
                'Amenity.2': Amenity(),
                'City.1': City(),
                'Place.1': Place(),
                'Place.2': Place(),
            }
            result = self.storage.count(cls)
            self.assertEqual(result, 2)

            result = self.storage.count()
            self.assertEqual(result, 5)


if __name__ == '__main__':
    unittest.main()