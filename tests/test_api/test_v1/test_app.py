#!/usr/bin/python3

"""Test api v1"""

from models.user import User
from models.state import State
from models.review import Review
from models.place import Place
from models.city import City
from models.amenity import Amenity
import models
import pep8
import unittest
from api.v1 import app
from api.v1.app import app as test_app

classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}

classes_test = {
    "User": {"first_name": "chuks", "last_name": "somzzy", "user_id": "save",
             "email": "somzzy@gmail.com", "password": "somzzy"},
    "State": {"name": "Lagos", "state_id": "save"},
    "City": {"name": "ojo", "state_id": None, "city_id": "save"},
    "Place": {"city_id": None, "user_id": None, "name":
              "Sheikh Murtadha str", "number_rooms": 3,
              "number_bathrooms": 2, "max_guest": 6,
              "price_by_night": 5000, "place_id": "save"},
    "Review": {"place_id": None, "user_id": None,
               "text": "Just Some test review", "review_id": "save"},
    "Amenity": {"name": "wifi", "amenity_id": "save"}
}


class TestApiDoc(unittest.TestCase):
    """Tests to check the documentation and style of app"""

    def test_pep8_conformance_app(self):
        """Test that api/v1/app.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['api/v1/app.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_app(self):
        """Test tests/test_api/test_v1/app.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(
            ['tests/test_api/test_v1/test_app.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_app_module_docstring(self):
        """Test for the app.py module docstring"""
        self.assertIsNot(app.__doc__, None,
                         "app.py needs a docstring")
        self.assertTrue(len(app.__doc__) >= 1,
                        "app.py needs a docstring")


class TestApiRoute(unittest.TestCase):
    """Test api routes """

    @classmethod
    def setUpClass(cls) -> None:
        """Setup Test Db with content"""
        id_store = {}
        cls.obj_insts = []
        for key, vals in classes_test.items():
            values = {}
            clss = classes[key]
            save_id = None
            for key, val in vals.items():
                if val == "save":
                    save_id = key
                elif not val:
                    values[key] = id_store[key]
                else:
                    values[key] = val
            obj_inst = clss(**values)
            obj_inst.save()
            cls.obj_insts.append(obj_inst)
            if save_id:
                id_store[save_id] = obj_inst.id

    @classmethod
    def tearDownClass(cls) -> None:
        """Teardown test Db after"""
        if cls.obj_insts:
            for obj in cls.obj_insts:
                models.storage.delete(obj)
        models.storage.save()
        models.storage.close()

    def setUp(self):
        """Setup app for testing"""
        test_app.testing = True
        self.app = test_app.test_client()

    def test_get_status(self):
        """Defines Test for status route"""
        res = self.app.get('/api/v1/status')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(res.json, {"status": "OK"})

    def test_get_stats(self):
        """"Defines Test for stats route"""
        res = self.app.get('/api/v1/stats')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content_type, "application/json")
        print(res.json)
        self.assertEqual(res.json, {
            'amenities': 1, 'cities': 1, 'places': 1,
            'reviews': 1, 'states': 1, 'users': 1})
