#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""
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
import pycodestyle
import unittest
import sqlalchemy
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
        pep8s = pycodestyle.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pycodestyle.StyleGuide(quiet=True)
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
    """"Test the DBstorage class"""

    def setUp(self):
        """initialize test environment"""
        self.storage = DBStorage()
        self.amenity = Amenity()
        self.city = City()
        self.place = Place()
        self.review = Review()
        self.state = State()
        self.user = User()

    def test_all_with_no_class(self):
        """test the all method with no class passed as argument"""
        self.storage.new(self.amenity)
        self.storage.new(self.city)
        self.storage.new(self.place)
        self.storage.new(self.review)
        self.storage.new(self.state)
        self.storage.new(self.user)
        self.storage.save()
        self.assertEqual(len(self.storage.all()), 6)

    def test_all_with_class(self):
        """test the all method with class passed as argument"""
        self.storage.new(self.amenity)
        self.storage.new(self.city)
        self.storage.new(self.place)
        self.storage.new(self.review)
        self.storage.new(self.state)
        self.storage.new(self.user)
        self.storage.save()
        self.assertEqual(len(self.storage.all(Amenity)), 1)
        self.assertEqual(len(self.storage.all(City)), 1)
        self.assertEqual(len(self.storage.all(Place)), 1)
        self.assertEqual(len(self.storage.all(Review)), 1)
        self.assertEqual(len(self.storage.all(State)), 1)
        self.assertEqual(len(self.storage.all(User)), 1)

    def test_get(self):
        """test the get method"""
        self.amenity.name = "Wi-Fi"
        self.storage.new(self.amenity)
        self.storage.save()
        self.assertIsInstance(self.storage.get(
            Amenity, self.amenity.id), Amenity)
        self.assertEqual(self.storage.get(
            Amenity, self.amenity.id).name, "Wi-Fi")
        self.assertIsNone(self.storage.get(Amenity, "fake_id"))
        self.assertIsNone(self.storage.get(City, self.amenity.id))

    def test_count(self):
        """test the count method"""
        self.storage.new(self.amenity)
        self.storage.new(self.city)
        self.storage.new(self.place)
        self.storage.new(self.review)
        self.storage.new(self.state)
        self.storage.new(self.user)
        self.storage.save()
        self.assertEqual(self.storage.count(), 6)
        self.assertEqual(self.storage.count(Amenity), 1)
        self.assertEqual(self.storage.count(City), 1)
        self.assertEqual(self.storage.count(Place), 1)
        self.assertEqual(self.storage.count(Review), 1)
        self.assertEqual(self.storage.count(State), 1)
        self.assertEqual(self.storage.count(User), 1)

    def test_new_save_delete(self):
        """test new, save and delete methods"""
        self.storage.new(self.amenity)
        self.storage.save()
        self.assertIsInstance(self.storage.get(
            Amenity, self.amenity.id), Amenity)
        self.storage.delete(self.amenity)
        self.storage.save()
        self.assertIsNone(self.storage.get(Amenity, self.amenity.id))

    def test_save_error(self):
        """test the save method with error"""
        self.amenity.name = None
        self.storage.new(self.amenity)
        with self.assertRaises(sqlalchemy.exc.IntegrityError):
            self.storage.save()

    def test_get_error(self):
        """test the get method with error"""
        with self.assertRaises(NameError):
            self.storage.get(None, "fake_id")


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


if __name__ == "__main__":
    unittest.main()
