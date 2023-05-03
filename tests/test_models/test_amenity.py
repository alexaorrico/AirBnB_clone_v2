import unittest
import os
from datetime import datetime
from models import *


class Test_AmenityModel(unittest.TestCase):
    """
    Test the amenity model class
    """

    def test_save(self):
        """test saving and retrieving an amenity"""
        test_args = {'updated_at': datetime(2017, 2, 12, 00, 31, 53, 331997),
                     'id': '054',
                     'created_at': datetime(2017, 2, 12, 00, 31, 53, 331900),
                     'name': "AMENITY SET UP"}
        model = Amenity(**test_args)
        model.save()
        all_amenities = storage.all("Amenity")
        self.assertIn(test_args['id'], all_amenities.keys())
        obj = storage.get("Amenity", test_args['id'])
        self.assertEqual(obj.name, test_args['name'])
        self.assertEqual(obj.created_at.hour, test_args['created_at'].hour)
        self.assertEqual(obj.updated_at.year, test_args['updated_at'].year)

    def test_var_initialization(self):
        """test the creation of the model went right"""
        test_args = {'updated_at': datetime(2017, 2, 12, 00, 31, 53, 331997),
                     'id': '055',
                     'created_at': datetime(2017, 2, 12, 00, 31, 53, 331900),
                     'name': "AMENITY SET UP"}
        model = Amenity(**test_args)
        self.assertEqual(model.name, test_args['name'])
        self.assertEqual(model.id, test_args['id'])
        self.assertEqual(model.created_at, test_args['created_at'])
        self.assertEqual(model.updated_at, test_args['updated_at'])

    def test_missing_arg(self):
        """test creating an Amenity with no argument"""
        new = Amenity()
        self.assertTrue(hasattr(new, "id"))
        self.assertTrue(hasattr(new, "created_at"))

    def test_date_format(self):
        """test the date has the right type"""
        model = Amenity()
        self.assertIsInstance(model.created_at, datetime)

    def test_delete(self):
        """test the deletion of an amenity"""
        model = Amenity(name="test_amenity_delete")
        model.save()
        self.assertIn(model.id, storage.all("Amenity").keys())
        storage.delete(model)
        self.assertIsNone(storage.get("Amenity", model.id))

    def test_all_amenity(self):
        """test querying all amenities"""
        length = storage.count("Amenity")
        a = Amenity(name="amenity1", id="id1")
        b = Amenity(name="amenity2", id="id2")
        a.save()
        b.save()
        all_amenities = storage.all("Amenity")
        self.assertIn(a.id, all_amenities.keys())
        self.assertIn(b.id, all_amenities.keys())
        self.assertEqual(storage.count("Amenity"), length + 2)

    def test_get_amenity(self):
        """test getting an amenity"""
        a = Amenity(name="test_get")
        id_a = a.id
        a.save()
        res = storage.get("Amenity", id_a)
        self.assertEqual(a.name, res.name)
        self.assertEqual(a.created_at.year, res.created_at.year)
        self.assertEqual(a.created_at.month, res.created_at.month)
        self.assertEqual(a.created_at.day, res.created_at.day)
        self.assertEqual(a.created_at.hour, res.created_at.hour)
        self.assertEqual(a.created_at.minute, res.created_at.minute)
        self.assertEqual(a.created_at.second, res.created_at.second)


if __name__ == "__main__":
    unittest.main()
