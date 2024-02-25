#!/usr/bin/python3
"""
Contains the TestCityDocs classes
"""

from datetime import datetime
import inspect
import models
from models import city
from models.base_model import BaseModel
import pep8
import unittest

City = city.City


class TestCityDocs(unittest.TestCase):
    """Tests to check the documentation and style of City class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.city_f = inspect.getmembers(City, inspect.isfunction)

    def test_pep8_conformance_city(self):
        """Test that models/city.py conforms to PEP8."""
        pep8style = pep8.StyleGuide(quiet=True)
        result = pep8style.check_files(["models/city.py"])
        self.assertEqual(
            result.total_errors, 0, "Found code style errors (and warnings)."
        )

    def test_pep8_conformance_test_city(self):
        """Test that tests/test_models/test_city.py conforms to PEP8."""
        pep8style = pep8.StyleGuide(quiet=True)
        result = pep8style.check_files(["tests/test_models/test_city.py"])
        self.assertEqual(
            result.total_errors, 0, "Found code style errors (and warnings)."
        )

    def test_city_module_docstring(self):
        """Test for the city.py module docstring"""
        self.assertTrue(len(city.__doc__) > 0)

    def test_city_class_docstring(self):
        """Test for the City class docstring"""
        self.assertTrue(len(City.__doc__) > 0)

    def test_city_func_docstrings(self):
        """Test for the presence of docstrings in City methods"""
        for func in self.city_f:
            self.assertTrue(len(func[1].__doc__) > 0)


class TestCity(unittest.TestCase):
    """Test the City class"""

    def test_is_subclass(self):
        """Test that City is a subclass of BaseModel"""
        city = City()
        self.assertIsInstance(city, BaseModel)

    def test_name_attr(self):
        """Test that City has attribute name, and it's an empty string"""
        city = City()
        self.assertTrue(hasattr(city, "name"))
        self.assertEqual(city.name, "")

    def test_state_id_attr(self):
        """Test that City has attribute state_id, and it's an empty string"""
        city = City()
        self.assertTrue(hasattr(city, "state_id"))
        self.assertEqual(city.state_id, "")

    def test_to_dict_creates_dict(self):
        """Test to_dict method creates a dictionary with proper attrs"""
        city = City()
        new_dict = city.to_dict()
        self.assertEqual(type(new_dict), dict)
        for attr in city.__dict__:
            if attr in new_dict:
                self.assertTrue(attr in new_dict)
                self.assertTrue(new_dict[attr] is not None)
        self.assertTrue("__class__" in new_dict)
        self.assertEqual(new_dict["__class__"], "City")

    def test_to_dict_values(self):
        """Test that values in to_dict match actual values"""
        city = City()
        new_dict = city.to_dict()
        self.assertEqual(new_dict["__class__"], "City")
        self.assertEqual(new_dict["id"], city.id)
        self.assertEqual(new_dict["created_at"], city.created_at.isoformat())
        self.assertEqual(new_dict["updated_at"], city.updated_at.isoformat())
        self.assertEqual(new_dict["name"], "")
        self.assertEqual(new_dict["state_id"], "")
        self.assertEqual(type(new_dict["created_at"]), str)
        self.assertEqual(type(new_dict["updated_at"]), str)
