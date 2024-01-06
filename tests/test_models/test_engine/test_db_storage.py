#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""
import unittest
import hashlib
import os
import inspect
import pep8
import models
from models.engine.db_storage import DBStorage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', 'Using FileStorage')
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
        path = 'tests/test_models/test_engine/test_db_storage.py'
        result = pep8s.check_files([path])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the DBStorage.py module docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage.py needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage.py needs a docstring")

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


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', 'Using FileStorage')
class TestClass_instantiation(unittest.TestCase):
    """Testing class instantiation"""

    def test_no_args(self):
        from models import storage
        self.assertEqual(type(storage), DBStorage)

    def test_args(self):
        with self.assertRaises(TypeError):
            DBStorage(None)

    def test_models_storage(self):
        from models import storage
        self.assertEqual(type(storage), DBStorage)


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', 'Using FileStorage')
class TestMethods(unittest.TestCase):
    """testing methods of the DBStorage class."""

    def setUp(self):
        from models import storage
        self.storage = storage

    def test_all_return_type(self):
        self.assertEqual(dict, type(self.storage.all()))

    def test_all_method_without_args(self):
        tafilalet = State(name="Tafilalet")
        errachidia = City(name="Errachidia", state_id=tafilalet.id)
        arfoud = City(name="Arfoud", state_id=tafilalet.id)

        tafilalet.save()
        errachidia.save()
        arfoud.save()

        dict_objs = self.storage.all()

        self.assertIn(tafilalet, dict_objs.values())
        self.assertIn(errachidia, dict_objs.values())
        self.assertIn(arfoud, dict_objs.values())

    def test_all_method_with_args(self):
        tafilalet = State(name="Tafilalet")
        errachidia = City(name="Errachidia", state_id=tafilalet.id)
        arfoud = City(name="Arfoud", state_id=tafilalet.id)

        tafilalet.save()
        errachidia.save()
        arfoud.save()

        # All states
        states_objs = self.storage.all(State)

        self.assertIn(tafilalet, states_objs.values())
        self.assertNotIn(errachidia, states_objs.values())
        self.assertNotIn(arfoud, states_objs.values())

        # All cities
        cities_objs = self.storage.all(City)

        self.assertNotIn(tafilalet, cities_objs.values())
        self.assertIn(errachidia, cities_objs.values())
        self.assertIn(arfoud, cities_objs.values())

    def test_new_method(self):
        state = State(name='Arizona')
        self.storage.new(state)
        self.assertIn("State." + state.id, self.storage.all().keys())
        self.assertIn(state, self.storage.all().values())

    def test_new_method_args(self):
        with self.assertRaises(TypeError):
            self.storage.new(State(name="Texas"), "testing")

    def test_save_method(self):
        state = State(name="Texas")
        self.storage.new(state)
        self.storage.save()
        self.assertIn("State." + state.id, self.storage.all().keys())
        self.assertIn(state, self.storage.all().values())

    def test_save_method_args(self):
        with self.assertRaises(TypeError):
            self.storage.save(None)

    def test_reload_method(self):
        state = State(name="Texas")

        self.storage.new(state)
        self.storage.save()
        self.storage.reload()
        storage_objs = self.storage.all()

        self.assertIn("State." + state.id, storage_objs)

    def test_reload_method_args(self):
        with self.assertRaises(TypeError):
            self.storage.reload(None)

    def test_delete(self):
        tafilalet = State(name="Tafilalet")
        errachidia = City(name="Errachidia", state_id=tafilalet.id)
        arfoud = City(name="Arfoud", state_id=tafilalet.id)

        tafilalet.save()
        errachidia.save()
        arfoud.save()

        dict_objs = self.storage.all()

        self.assertIn(tafilalet, dict_objs.values())
        self.assertIn(errachidia, dict_objs.values())
        self.assertIn(arfoud, dict_objs.values())

        self.storage.delete(errachidia)

        dict_objs = self.storage.all()

        self.assertIn(tafilalet, dict_objs.values())
        self.assertNotIn(errachidia, dict_objs.values())
        self.assertIn(arfoud, dict_objs.values())

        self.storage.delete(tafilalet)

        dict_objs = self.storage.all()

        self.assertNotIn(tafilalet, dict_objs.values())
        self.assertNotIn(errachidia, dict_objs.values())
        self.assertNotIn(arfoud, dict_objs.values())


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', 'Using FileStorage')
class TestWithUser(unittest.TestCase):
    """testing that DBStorage class correctly handles User class"""

    def setUp(self):
        from models import storage
        self.storage = storage

    def test_new_method(self):
        obj = User(email='john_doe@baz.com', password='mlmlml',
                   first_name='John', last_name='Doe')
        self.storage.new(obj)
        self.assertIn("User." + obj.id, self.storage.all().keys())
        self.assertIn(obj, self.storage.all().values())

    def test_save_method(self):
        obj = User(email='john_doe@baz.com', password='mlmlml',
                   first_name='John', last_name='Doe')
        self.storage.new(obj)
        self.storage.save()
        self.assertIn("User." + obj.id, self.storage.all().keys())
        self.assertIn(obj, self.storage.all().values())

    def test_reload_method(self):
        obj = User(email='john_doe@baz.com', password='mlmlml',
                   first_name='John', last_name='Doe')
        key = "User." + obj.id

        self.storage.new(obj)
        self.storage.save()
        self.storage.reload()
        storage_objs = self.storage.all()

        self.assertIn(key, storage_objs)
        self.assertEqual(storage_objs[key].id, obj.id)
        self.assertEqual(storage_objs[key].password,
                         hashlib.md5(str('mlmlml').encode()).hexdigest())


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', 'Using FileStorage')
class TestWithState(unittest.TestCase):
    """testing that DBStorage class correctly handles State class"""

    def setUp(self):
        from models import storage
        self.storage = storage

    def test_new_method(self):
        obj = State(name="Texas")
        self.storage.new(obj)
        self.assertIn("State." + obj.id, self.storage.all().keys())
        self.assertIn(obj, self.storage.all().values())

    def test_save_method(self):
        obj = State(name="Texas")
        self.storage.new(obj)
        self.storage.save()
        self.assertIn("State." + obj.id, self.storage.all().keys())
        self.assertIn(obj, self.storage.all().values())

    def test_reload_method(self):
        obj = State(name="Texas")
        key = "State." + obj.id
        obj.name = 'California'

        self.storage.new(obj)
        self.storage.save()
        self.storage.reload()
        storage_objs = self.storage.all()

        self.assertIn(key, storage_objs)
        self.assertEqual(storage_objs[key].id, obj.id)
        self.assertEqual(storage_objs[key].name, 'California')


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', 'Using FileStorage')
class TestWithCity(unittest.TestCase):
    """testing that DBStorage class correctly handles City class"""

    def setUp(self):
        from models import storage
        self.storage = storage

        self.arizona = State(name='Arizona')
        self.arizona.save()

    def test_new_method(self):
        obj = City(name='San Jose', state_id=self.arizona.id)
        self.storage.new(obj)
        self.assertIn("City." + obj.id, self.storage.all().keys())
        self.assertIn(obj, self.storage.all().values())

    def test_save_method(self):
        obj = City(name='San Jose', state_id=self.arizona.id)
        self.storage.new(obj)
        self.storage.save()
        self.assertIn("City." + obj.id, self.storage.all().keys())
        self.assertIn(obj, self.storage.all().values())

    def test_reload_method(self):
        obj = City(name='San Jose', state_id=self.arizona.id)
        key = "City." + obj.id

        self.storage.new(obj)
        self.storage.save()
        self.storage.reload()
        storage_objs = self.storage.all()

        self.assertIn(key, storage_objs)
        self.assertEqual(storage_objs[key].id, obj.id)
        self.assertEqual(storage_objs[key].name, 'San Jose')


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', 'Using FileStorage')
class TestWithPlace(unittest.TestCase):
    """testing that DBStorage class correctly handles Place class"""

    def setUp(self):
        from models import storage
        self.storage = storage

        self.arizona = State(name='Arizona')
        self.arizona.save()

        self.san_jose = City(name='San Jose', state_id=self.arizona.id)
        self.san_jose.save()

        self.john_doe = User(email='john_doe@baz.com', password='mlmlml',
                             first_name='John', last_name='Doe')
        self.john_doe.save()

    def test_new_method(self):
        obj = Place(name='Huge House', description='Sweet home',
                    city_id=self.san_jose.id,
                    user_id=self.john_doe.id)
        self.storage.new(obj)
        self.assertIn("Place." + obj.id, self.storage.all().keys())
        self.assertIn(obj, self.storage.all().values())

    def test_save_method(self):
        obj = Place(name='Huge House', description='Sweet home',
                    city_id=self.san_jose.id,
                    user_id=self.john_doe.id)
        self.storage.new(obj)
        self.storage.save()
        self.assertIn("Place." + obj.id, self.storage.all().keys())
        self.assertIn(obj, self.storage.all().values())

    def test_reload_method(self):
        obj = Place(name='Huge House', description='Sweet home',
                    city_id=self.san_jose.id,
                    user_id=self.john_doe.id)
        key = "Place." + obj.id
        obj.latitude = 77.8
        obj.longitude = 45.23

        amenity_1 = Amenity(name="Wifi")
        amenity_1.save()
        amenity_2 = Amenity(name="Cable")
        amenity_2.save()
        amenity_3 = Amenity(name="Oven")
        amenity_3.save()

        obj.amenities.append(amenity_1)
        obj.amenities.append(amenity_2)
        obj.amenities.append(amenity_3)

        self.storage.new(obj)
        self.storage.save()
        storage_objs = self.storage.all()

        self.assertIn(key, storage_objs)

        self.assertEqual(type(storage_objs[key].id), str)
        self.assertEqual(storage_objs[key].id, obj.id)

        self.assertEqual(type(storage_objs[key].name), str)
        self.assertEqual(storage_objs[key].name, 'Huge House')

        self.assertEqual(type(storage_objs[key].description), str)
        self.assertEqual(storage_objs[key].description, 'Sweet home')

        self.assertEqual(type(storage_objs[key].latitude), float)
        self.assertEqual(storage_objs[key].latitude, 77.8)

        self.assertEqual(type(storage_objs[key].longitude), float)
        self.assertEqual(storage_objs[key].longitude, 45.23)

        self.assertIn(amenity_1, storage_objs[key].amenities)
        self.assertIn(amenity_2, storage_objs[key].amenities)
        self.assertIn(amenity_3, storage_objs[key].amenities)


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', 'Using FileStorage')
class TestWithAmenity(unittest.TestCase):
    """testing that DBStorage class correctly handles Amenity class"""

    def setUp(self):

        from models import storage
        self.storage = storage

    def test_new_method(self):
        obj = Amenity(name='Kitchen')
        self.storage.new(obj)
        self.assertIn("Amenity." + obj.id, self.storage.all().keys())
        self.assertIn(obj, self.storage.all().values())

    def test_save_method(self):
        obj = Amenity(name='Kitchen')
        self.storage.new(obj)
        self.storage.save()
        self.assertIn("Amenity." + obj.id, self.storage.all().keys())
        self.assertIn(obj, self.storage.all().values())

    def test_reload_method(self):
        obj = Amenity(name='Kitchen')
        key = "Amenity." + obj.id

        self.storage.new(obj)
        self.storage.save()
        self.storage.reload()
        storage_objs = self.storage.all()

        self.assertIn(key, storage_objs)
        self.assertEqual(storage_objs[key].id, obj.id)
        self.assertEqual(storage_objs[key].name, 'Kitchen')


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', 'Using FileStorage')
class TestWithReview(unittest.TestCase):
    """testing that DBStorage class correctly handles Review class"""

    def setUp(self):
        from models import storage
        self.storage = storage

        self.arizona = State(name='Arizona')
        self.arizona.save()

        self.san_jose = City(name='San Jose', state_id=self.arizona.id)
        self.san_jose.save()

        self.john_doe = User(email='john_doe@baz.com', password='mlmlml',
                             first_name='John', last_name='Doe')
        self.john_doe.save()

        self.huge_house = Place(name='Huge House', description='Sweet home',
                                city_id=self.san_jose.id,
                                user_id=self.john_doe.id)
        self.huge_house.save()

    def test_new_method(self):
        obj = Review(text='Excellent', user_id=self.john_doe.id,
                     place_id=self.huge_house.id)
        self.storage.new(obj)
        self.assertIn("Review." + obj.id, self.storage.all().keys())
        self.assertIn(obj, self.storage.all().values())

    def test_save_method(self):
        obj = Review(text='Excellent', user_id=self.john_doe.id,
                     place_id=self.huge_house.id)
        self.storage.new(obj)
        self.storage.save()
        self.assertIn("Review." + obj.id, self.storage.all().keys())
        self.assertIn(obj, self.storage.all().values())

    def test_reload_method(self):
        obj = Review(text='Excellent', user_id=self.john_doe.id,
                     place_id=self.huge_house.id)
        key = "Review." + obj.id

        self.storage.new(obj)
        self.storage.save()
        self.storage.reload()
        storage_objs = self.storage.all()

        self.assertIn(key, storage_objs)
        self.assertEqual(storage_objs[key].id, obj.id)
        self.assertEqual(storage_objs[key].text, 'Excellent')


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', 'Using FileStorage')
class TestGetCount(unittest.TestCase):
    """testing DBStorage's get() and count() methods"""

    def setUp(self):
        from models import storage
        self.storage = storage

    def test_get(self):
        """test that get(obj) correctly retrieves obj from the storage"""
        user = User(email="user@example.com", password="passwd")
        user.save()

        objs_dict = self.storage.all()

        retrieved_user = self.storage.get(User, user.id)
        self.assertEqual(retrieved_user.id, user.id)
        self.assertEqual(retrieved_user.email, user.email)
        self.assertEqual(retrieved_user.password, user.password)

        state = State(name="Texas")

        retrieved_state = self.storage.get(State, state.id)
        self.assertIsNone(retrieved_state)

    def test_count(self):
        """test that count([cls]) correctly counts the self.storage obj"""

        self.assertEqual(self.storage.count(), 0)

        user1 = User(email="user1@example.com", password="passwd")
        user2 = User(email="user2@example.com", password="dwssap")
        state = State(name="Texas")
        user1.save()
        user2.save()
        state.save()

        self.assertEqual(self.storage.count(), 3)
        self.assertEqual(self.storage.count(User), 2)
        self.assertEqual(self.storage.count(State), 1)
        self.assertEqual(self.storage.count(City), 0)
