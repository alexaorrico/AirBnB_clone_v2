from datetime import datetime
from models import *
import os
import unittest


class Test_CityModel(unittest.TestCase):
    """
    Test the city model class
    """
    @classmethod
    def setUpClass(cls):
        """Create a State object to test City"""
        test_state = {'updated_at': datetime(2017, 2, 12, 00, 31, 50, 331997),
                      'id': "001",
                      'created_at': datetime(2017, 2, 12, 00, 31, 55, 331997),
                      'name': "TEST STATE FOR CITY"}
        cls.state = State(test_state)
        cls.state.save()

    @classmethod
    def tearDownClass(cls):
        storage.delete(cls.state)

    def test_save(self):
        """Set up the variables before the test"""
        test_args = {'updated_at': datetime(2017, 2, 12, 00, 31, 53, 331997),
                     'id': 'f519fb40-1f5c-458b-945c-2ee8eaaf4900',
                     'created_at': datetime(2017, 2, 12, 00, 31, 53, 331900),
                     'name': "CITY SET UP",
                     'state_id': "001"}
        model = City(test_args)
        model.save()
        all_cities = storage.all("City")
        self.assertIn(test_args['id'], all_cities.keys())
        obj = storage.get("City", test_args['id'])
        self.assertEqual(obj.name, test_args['name'])
        self.assertEqual(obj.created_at.hour, test_args['created_at'].hour)
        self.assertEqual(obj.updated_at.year, test_args['updated_at'].year)

    def test_var_initialization(self):
        """test simple initialization"""
        test_args = {'updated_at': datetime(2017, 2, 12, 00, 31, 53, 331997),
                     'id': 'f519fb40-1f5c-458b-945c-2ee8eaaf4900',
                     'created_at': datetime(2017, 2, 12, 00, 31, 53, 331900),
                     'name': "CITY SET UP",
                     'state_id': "001"}
        model = City(test_args)
        self.assertEqual(model.name, test_args['name'])
        self.assertEqual(model.id, test_args['id'])
        self.assertEqual(model.created_at, test_args['created_at'])
        self.assertEqual(model.updated_at, test_args['updated_at'])

    def test_initialization_no_arg(self):
        """test initialization without arguments"""
        new = City()
        self.assertTrue(hasattr(new, "state_id"))
        self.assertTrue(hasattr(new, "created_at"))

    def test_date_format(self):
        """test the date has the right type"""
        model = City()
        self.assertIsInstance(model.created_at, datetime)

    def test_delete(self):
        """test the deletion of a city"""
        model = City(name="test_city_delete", state_id="001")
        model.save()
        self.assertIn(model.id, storage.all("City").keys())
        storage.delete(model)
        self.assertIsNone(storage.get("City", model.id))

    def test_all_city(self):
        """test querying all cities"""
        length = storage.count("City")
        a = City(name="amenity1", id="id1", state_id="001")
        b = City(name="amenity2", id="id2", state_id="001")
        a.save()
        b.save()
        all_cities = storage.all("City")
        self.assertIn(a.id, all_cities.keys())
        self.assertIn(b.id, all_cities.keys())
        self.assertEqual(storage.count("City"), length + 2)

    def test_get_city(self):
        """test getting an amenity"""
        a = City(name="test_get", state_id="001")
        id_a = a.id
        a.save()
        res = storage.get("City", id_a)
        self.assertEqual(a.name, res.name)
        self.assertEqual(a.created_at.year, res.created_at.year)
        self.assertEqual(a.created_at.month, res.created_at.month)
        self.assertEqual(a.created_at.day, res.created_at.day)
        self.assertEqual(a.created_at.hour, res.created_at.hour)
        self.assertEqual(a.created_at.minute, res.created_at.minute)
        self.assertEqual(a.created_at.second, res.created_at.second)


if __name__ == "__main__":
    unittest.main()
