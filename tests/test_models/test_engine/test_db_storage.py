#!/usr/bin/python3
"""
Unit Test for BaseModel Class
"""
import unittest
from datetime import datetime
from models import *
import os
from models.base_model import Base
from models.engine.db_storage import DBStorage


storage_type = os.environ.get('HBNB_TYPE_STORAGE')


@unittest.skipIf(storage_type != 'db', 'skip if environ is not db')
class TestDBStorageDocs(unittest.TestCase):
    """Class for testing BaseModel docs"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('..... Testing Documentation .....')
        print('..... For FileStorage Class .....')
        print('.................................\n\n')

    def test_doc_file(self):
        """... documentation for the file"""
        expected = ' Database engine '
        actual = db_storage.__doc__
        self.assertEqual(expected, actual)

    def test_doc_class(self):
        """... documentation for the class"""
        expected = 'handles long term storage of all class instances'
        actual = DBStorage.__doc__
        self.assertEqual(expected, actual)

    def test_doc_all(self):
        """... documentation for all function"""
        expected = ' returns a dictionary of all objects '
        actual = DBStorage.all.__doc__
        self.assertEqual(expected, actual)

    def test_doc_new(self):
        """... documentation for new function"""
        expected = ' adds objects to current database session '
        actual = DBStorage.new.__doc__
        self.assertEqual(expected, actual)

    def test_doc_save(self):
        """... documentation for save function"""
        expected = ' commits all changes of current database session '
        actual = DBStorage.save.__doc__
        self.assertEqual(expected, actual)

    def test_doc_reload(self):
        """... documentation for reload function"""
        expected = ' creates all tables in database & session from engine '
        actual = DBStorage.reload.__doc__
        self.assertEqual(expected, actual)

    def test_doc_delete(self):
        """... documentation for delete function"""
        expected = ' deletes obj from current database session if not None '
        actual = DBStorage.delete.__doc__
        self.assertEqual(expected, actual)

    def test_doc_get(self):
        """... documentation for get function"""
        expected = ' retrieves one object '
        actual = DBStorage.get.__doc__
        self.assertEqual(expected, actual)

    def test_doc_count(self):
        """... testing length version of count function
        """
        expected = 293
        actual = len(DBStorage.count.__doc__)
        self.assertEqual(expected, actual)


@unittest.skipIf(storage_type != 'db', 'skip if environ is not db')
class TestStateDBInstances(unittest.TestCase):
    """testing for class instances"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('......... Testing DBStorage .;.......')
        print('........ For State Class ........')
        print('.................................\n\n')

    def setUp(self):
        """initializes new BaseModel object for testing"""
        self.state = State()
        self.state.name = 'California'
        self.state.save()

    def test_state_all(self):
        """... checks if all() function returns newly created instance"""
        all_objs = storage.all()
        all_state_objs = storage.all('State')

        exist_in_all = False
        for k in all_objs.keys():
            if self.state.id in k:
                exist_in_all = True
        exist_in_all_states = False
        for k in all_state_objs.keys():
            if self.state.id in k:
                exist_in_all_states = True

        self.assertTrue(exist_in_all)
        self.assertTrue(exist_in_all_states)

    def test_state_delete(self):
        state_id = self.state.id
        storage.delete(self.state)
        self.state = None
        storage.save()
        exist_in_all = False
        for k in storage.all().keys():
            if state_id in k:
                exist_in_all = True
        self.assertFalse(exist_in_all)


@unittest.skipIf(storage_type != 'db', 'skip if environ is not db')
class TestUserDBInstances(unittest.TestCase):
    """testing for class instances"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('...... Testing FileStorage ......')
        print('.......... User  Class ..........')
        print('.................................\n\n')

    def setUp(self):
        """initializes new user for testing"""
        self.user = User()
        self.user.email = 'test'
        self.user.password = 'test'
        self.user.save()

    def test_user_all(self):
        """... checks if all() function returns newly created instance"""
        all_objs = storage.all()
        all_user_objs = storage.all('User')

        exist_in_all = False
        for k in all_objs.keys():
            if self.user.id in k:
                exist_in_all = True
        exist_in_all_users = False
        for k in all_user_objs.keys():
            if self.user.id in k:
                exist_in_all_users = True

        self.assertTrue(exist_in_all)
        self.assertTrue(exist_in_all_users)

    def test_user_delete(self):
        user_id = self.user.id
        storage.delete(self.user)
        self.user = None
        storage.save()
        exist_in_all = False
        for k in storage.all().keys():
            if user_id in k:
                exist_in_all = True
        self.assertFalse(exist_in_all)


@unittest.skipIf(storage_type != 'db', 'skip if environ is not db')
class TestCityDBInstances(unittest.TestCase):
    """testing for class instances"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('...... Testing DBStorage ......')
        print('.......... City  Class ..........')
        print('.................................\n\n')

    def setUp(self):
        """initializes new user for testing"""
        self.state = State()
        self.state.name = 'California'
        self.state.save()
        self.city = City()
        self.city.name = 'Fremont'
        self.city.state_id = self.state.id
        self.city.save()

    def test_city_all(self):
        """... checks if all() function returns newly created instance"""
        all_objs = storage.all()
        all_city_objs = storage.all('City')

        exist_in_all = False
        for k in all_objs.keys():
            if self.city.id in k:
                exist_in_all = True
        exist_in_all_city = False
        for k in all_city_objs.keys():
            if self.city.id in k:
                exist_in_all_city = True

        self.assertTrue(exist_in_all)
        self.assertTrue(exist_in_all_city)


@unittest.skipIf(storage_type != 'db', 'skip if environ is not db')
class TestCityDBInstancesUnderscore(unittest.TestCase):
    """testing for class instances"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('...... Testing FileStorage ......')
        print('.......... City Class ..........')
        print('.................................\n\n')

    def setUp(self):
        """initializes new user for testing"""
        self.state = State()
        self.state.name = 'California'
        self.state.save()
        self.city = City()
        self.city.name = 'San_Francisco'
        self.city.state_id = self.state.id
        self.city.save()

    def test_city_underscore_all(self):
        """... checks if all() function returns newly created instance"""
        all_objs = storage.all()
        all_city_objs = storage.all('City')

        exist_in_all = False
        for k in all_objs.keys():
            if self.city.id in k:
                exist_in_all = True
        exist_in_all_city = False
        for k in all_city_objs.keys():
            if self.city.id in k:
                exist_in_all_city = True

        self.assertTrue(exist_in_all)
        self.assertTrue(exist_in_all_city)


@unittest.skipIf(storage_type != 'db', 'skip if environ is not db')
class TestPlaceDBInstances(unittest.TestCase):
    """testing for class instances"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('...... Testing DBStorage ......')
        print('.......... Place  Class ..........')
        print('.................................\n\n')

    def setUp(self):
        """initializes new user for testing"""
        self.user = User()
        self.user.email = 'test'
        self.user.password = 'test'
        self.user.save()
        self.state = State()
        self.state.name = 'California'
        self.state.save()
        self.city = City()
        self.city.name = 'San_Mateo'
        self.city.state_id = self.state.id
        self.city.save()
        self.place = Place()
        self.place.city_id = self.city.id
        self.place.user_id = self.user.id
        self.place.name = 'test_place'
        self.place.description = 'test_description'
        self.place.number_rooms = 2
        self.place.number_bathrooms = 1
        self.place.max_guest = 4
        self.place.price_by_night = 100
        self.place.latitude = 120.12
        self.place.longitude = 101.4
        self.place.save()

    def test_place_all(self):
        """... checks if all() function returns newly created instance"""
        all_objs = storage.all()
        all_place_objs = storage.all('Place')

        exist_in_all = False
        for k in all_objs.keys():
            if self.place.id in k:
                exist_in_all = True
        exist_in_all_place = False
        for k in all_place_objs.keys():
            if self.place.id in k:
                exist_in_all_place = True

        self.assertTrue(exist_in_all)
        self.assertTrue(exist_in_all_place)


@unittest.skipIf(storage_type != 'db', 'skip if environ is not db')
class TestGetCountDB(unittest.TestCase):
    """testing get and count methods"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('...... Testing Get and Count ......')
        print('.......... DB Methods ..........')
        print('.................................\n\n')

    def setUp(self):
        """initializes new state and cities for testing"""
        self.state = State()
        self.state.name = 'California'
        self.state.save()
        self.city1 = City()
        self.city1.name = 'Fremont'
        self.city1.state_id = self.state.id
        self.city1.save()
        self.city2 = City()
        self.city2.name = 'San_Francisco'
        self.city2.state_id = self.state.id
        self.city2.save()

    def test_get(self):
        """check if get method returns state"""
        real_state = storage.get("State", self.state.id)
        fake_state = storage.get("State", "12345")
        no_state = storage.get("", "")

        self.assertEqual(real_state, self.state)
        self.assertNotEqual(fake_state, self.state)
        self.assertIsNone(no_state)

    def test_count(self):
        """checks if count method returns correct numbers"""
        state_count = storage.count("State")
        city_count = storage.count("City")
        place_count = storage.count("Place")
        all_count = storage.count("")

        self.assertEqual(state_count, 3)
        self.assertEqual(city_count, 4)
        self.assertEqual(place_count, 0)
        self.assertEqual(all_count, 7)

if __name__ == '__main__':
    unittest.main
