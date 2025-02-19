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
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/amenity.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_amenity(self):
        """Test that tests/test_models/test_amenity.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_amenity.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_amenity_module_docstring(self):
        """Test for the amenity.py module docstring"""
        self.assertIsNot(amenity.__doc__, None,
                         "amenity.py needs a docstring")
        self.assertTrue(len(amenity.__doc__) >= 1,
                        "amenity.py needs a docstring")

    def test_amenity_class_docstring(self):
        """Test for the Amenity class docstring"""
        self.assertIsNot(Amenity.__doc__, None,
                         "Amenity class needs a docstring")
        self.assertTrue(len(Amenity.__doc__) >= 1,
                        "Amenity class needs a docstring")

    def test_amenity_func_docstrings(self):
        """Test for the presence of docstrings in Amenity methods"""
        for func in self.amenity_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestAmenity(unittest.TestCase):
    """Test the Amenity class"""

    def test_is_subclass(self):
        """Test that Amenity is a subclass of BaseModel"""
        amenity = Amenity()
        self.assertIsInstance(amenity, BaseModel)
        self.assertTrue(hasattr(amenity, "id"))
        self.assertTrue(hasattr(amenity, "created_at"))
        self.assertTrue(hasattr(amenity, "updated_at"))

    def test_name_attr(self):
        """Test that Amenity has attribute name, and it's as an empty string"""
        amenity = Amenity()
        self.assertTrue(hasattr(amenity, "name"))
        if models.storage_t == 'db':
            self.assertEqual(amenity.name, None)
        else:
            self.assertEqual(amenity.name, "")

    def test_to_dict_creates_dict(self):
        """test to_dict method creates a dictionary with proper attrs"""
#         am = Amenity()
#         new_d = am.to_dict()
#         self.assertEqual(type(new_d), dict)
#         self.assertFalse("_sa_instance_state" in new_d)
#         for attr in am.__dict__:
#             if attr is not "_sa_instance_state":
#                 self.assertTrue(attr in new_d)
#         self.assertTrue("__class__" in new_d)

        #   new_amenity = Amenity()
        #   expected_attrs = [
        #    "id",
        #    "created_at",
        #    "updated_at",
        #    "__class__",
        #    "name"]
        #   d = new_amenity.to_dict()
        #   self.assertTrue(all(attr in d for attr in expected_attrs))

        am = Amenity()
        am.name = "Wifi"
        d = am.to_dict()
        expected_attrs = [
            "id",
            "created_at",
            "updated_at",
            "name",
            "__class__"]
        self.assertTrue(all(attr in d for attr in expected_attrs))

    def test_to_dict_values(self):
        """test that values in dict returned from to_dict are correct"""
#         am = Amenity()
#         new_d = am.to_dict()
#         self.assertEqual(new_d.get("__class__"), "Amenity")
#         self.assertTrue(isinstance(new_d.get("created_at"), str))
#         self.assertTrue(isinstance(new_d.get("updated_at"), str))
#
#         created_at_str = new_d.get("created_at")
#         updated_at_str = new_d.get("updated_at")
#
#         self.assertIsNotNone(created_at_str)
#         self.assertIsNotNone(updated_at_str)
#
#         # If created_at and updated_at are not None,
#         ensure they match expected
#         # format
#         if created_at_str and updated_at_str:
#             t_format = "%Y-%m-%dT%H:%M:%S.%f"
#             created_at = datetime.strptime(created_at_str, t_format)
#             updated_at = datetime.strptime(updated_at_str, t_format)
#             self.assertEqual(created_at, am.created_at)
#             self.assertEqual(updated_at, am.updated_at)

        #   new_amenity = Amenity()
        #   d = new_amenity.to_dict()
        #   self.assertEqual(d["__class__"], "Amenity")
        #   self.assertEqual(d["name"], new_amenity.name)
        #   self.assertTrue(isinstance(d.get("created_at"), str))
        #   self.assertTrue(isinstance(d.get("updated_at"), str))

        am = Amenity()
        am.name = "Wifi"
        d = am.to_dict()
        self.assertEqual(d["name"], "Wifi")

    def test_str(self):
        """test that the str method has the correct output"""
        amenity = Amenity()
        string = "[Amenity] ({}) {}".format(amenity.id, amenity.__dict__)
        self.assertEqual(string, str(amenity))

    def test_save(self):
        """Test that save method updates `updated_at` attribute"""
        am = Amenity()
        old_updated_at = am.updated_at
        am.save()
        self.assertNotEqual(am.updated_at, old_updated_at)

    def test_initialization_with_kwargs(self):
        """Test initialization of Amenity with kwargs"""
        dt = datetime.now().isoformat()
        am = Amenity(id="123", created_at=dt, updated_at=dt, name="Pool")
        self.assertEqual(am.id, "123")
        self.assertEqual(am.created_at.isoformat(), dt)
        self.assertEqual(am.updated_at.isoformat(), dt)
        self.assertEqual(am.name, "Pool")

    def test_unique_ids(self):
        """Test that each Amenity has a unique id"""
        am1 = Amenity()
        am2 = Amenity()
        self.assertNotEqual(am1.id, am2.id)

    def test_storage_of_new_instance(self):
        """Test that new instance is stored in storage"""
        am = Amenity()
        am.save()
        self.assertIn(am, models.storage.all().values())

    def test_name_initialization(self):
        """Test that name attribute is correctly set during initialization"""
        name = "Test Amenity"
        am = Amenity(name=name)
        self.assertEqual(am.name, name)
