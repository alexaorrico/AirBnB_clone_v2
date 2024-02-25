#!/usr/bin/python3
"""
Contains the TestAmenityDocs classes
"""

from datetime import datetime
import inspect
import models
from models import amenity
from models.base_model import BaseModel
import pep8
import unittest

Amenity = amenity.Amenity


class TestAmenityDocs(unittest.TestCase):
    """Tests to check the documentation and style of Amenity class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.amenity_f = inspect.getmembers(Amenity, inspect.isfunction)

    def test_pep8_conformance_amenity(self):
        """Test that models/amenity.py conforms to PEP8."""
        pep8style = pep8.StyleGuide(quiet=True)
        result = pep8style.check_files(["models/amenity.py"])
        self.assertEqual(
            result.total_errors, 0, "Found code style errors (and warnings)."
        )

    def test_pep8_conformance_test_amenity(self):
        """Test that tests/test_models/test_amenity.py conforms to PEP8."""
        pep8style = pep8.StyleGuide(quiet=True)
        result = pep8style.check_files(["tests/test_models/test_amenity.py"])
        self.assertEqual(
            result.total_errors, 0, "Found code style errors (and warnings)."
        )

    def test_amenity_module_docstring(self):
        """Test for the amenity.py module docstring"""
        self.assertTrue(len(amenity.__doc__) > 0)

    def test_amenity_class_docstring(self):
        """Test for the Amenity class docstring"""
        self.assertTrue(len(Amenity.__doc__) > 0)

    def test_amenity_func_docstrings(self):
        """Test for the presence of docstrings in Amenity methods"""
        for func in self.amenity_f:
            self.assertTrue(len(func[1].__doc__) > 0)


class TestAmenity(unittest.TestCase):
    """Test the Amenity class"""

    def test_is_subclass(self):
        """Test that Amenity is a subclass of BaseModel"""
        amenity = Amenity()
        self.assertIsInstance(amenity, BaseModel)

    def test_name(self):
        """Test that Amenity has attribute name, and it's an empty string"""
        amenity = Amenity()
        self.assertTrue(hasattr(amenity, "name"))
        self.assertEqual(amenity.name, "")

    def test_to_dict_creates_dict(self):
        """Test that to_dict method creates a dictionary with proper attrs"""
        amenity = Amenity()
        new_dict = amenity.to_dict()
        self.assertEqual(type(new_dict), dict)
        for attr in amenity.__dict__:
            if attr is "_sa_instance_state":
                continue
            self.assertTrue(attr in new_dict)
        self.assertTrue("__class__" in new_dict)
        self.assertTrue("to_dict" in dir(amenity))
