#!/usr/bin/python3
"""
Contains the TestPlaceDocs classes
"""

from datetime import datetime
import inspect
import models
from models import place
from models.base_model import BaseModel
import pep8
import unittest

Place = place.Place


class TestPlaceDocs(unittest.TestCase):
    """Tests to check the documentation and style of Place class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.place_f = inspect.getmembers(Place, inspect.isfunction)

    def test_pep8_conformance_place(self):
        """Test that models/place.py conforms to PEP8."""
        pep8style = pep8.StyleGuide(quiet=True)
        result = pep8style.check_files(["models/place.py"])
        self.assertEqual(
            result.total_errors, 0, "Found code style errors (and warnings)."
        )

    def test_pep8_conformance_test_place(self):
        """Test that tests/test_models/test_place.py conforms to PEP8."""
        pep8style = pep8.StyleGuide(quiet=True)
        result = pep8style.check_files(["tests/test_models/test_place.py"])
        self.assertEqual(
            result.total_errors, 0, "Found code style errors (and warnings)."
        )

    def test_place_module_docstring(self):
        """Test for the place.py module docstring"""
        self.assertTrue(len(place.__doc__) > 0)

    def test_place_class_docstring(self):
        """Test for the Place class docstring"""
        self.assertTrue(len(Place.__doc__) > 0)

    def test_place_func_docstrings(self):
        """Test for the presence of docstrings in Place methods"""
        for func in self.place_f:
            self.assertTrue(len(func[1].__doc__) > 0)


class TestPlace(unittest.TestCase):
    """Test the Place class"""

    def test_is_subclass(self):
        """Test that Place is a subclass of BaseModel"""
        place = Place()
        self.assertIsInstance(place, BaseModel)

    def test_city_id_attr(self):
        """Test that Place has attribute city_id, and it's an empty string"""
        place = Place()
        self.assertTrue(hasattr(place, "city_id"))
        self.assertEqual(place.city_id, "")

    def test_user_id_attr(self):
        """Test that Place has attribute user_id, and it's an empty string"""
        place = Place()
        self.assertTrue(hasattr(place, "user_id"))
        self.assertEqual(place.user_id, "")

    def test_name_attr(self):
        """Test that Place has attribute name, and it's an empty string"""
        place = Place()
        self.assertTrue(hasattr(place, "name"))
        self.assertEqual(place.name, "")

    def test_description_attr(self):
        """Test that Place has attribute description,
        and it's an empty string"""
        place = Place()
        self.assertTrue(hasattr(place, "description"))
        self.assertEqual(place.description, "")

    def test_number_rooms_attr(self):
        """Test that Place has attribute number_rooms, and it's an int == 0"""
        place = Place()
        self.assertTrue(hasattr(place, "number_rooms"))
        self.assertEqual(place.number_rooms, 0)

    def test_number_bathrooms_attr(self):
        """Test that Place has attribute number_bathrooms,
        and it's an int == 0"""
        place = Place()
        self.assertTrue(hasattr(place, "number_bathrooms"))
        self.assertEqual(place.number_bathrooms, 0)

    def test_max_guest_attr(self):
        """Test that Place has attribute max_guest, and it's an int == 0"""
        place = Place()
        self.assertTrue(hasattr(place, "max_guest"))
        self.assertEqual(place.max_guest, 0)

    def test_price_by_night_attr(self):
        """Test that Place has attribute price_by_night,
        and it's an int == 0"""
        place = Place()
        self.assertTrue(hasattr(place, "price_by_night"))
        self.assertEqual(place.price_by_night, 0)

    def test_latitude_attr(self):
        """Test that Place has attribute latitude, and it's a float == 0.0"""
        place = Place()
        self.assertTrue(hasattr(place, "latitude"))
        self.assertEqual
