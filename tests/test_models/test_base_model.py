#!/usr/bin/python3
"""
Contains class TestBaseModelDocs and class TestBaseModel
"""


from datetime import datetime
import inspect
from models import base_model
import pep8
import unittest
import string
BaseModel = base_model.BaseModel


class TestBaseModelDocs(unittest.TestCase):
    """Tests to check the documentation and style of BaseModel class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.base_f = inspect.getmembers(BaseModel, inspect.isfunction)

    def test_pep8_conformance_base_model(self):
        """Test that models/base_model.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/base_model.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_base_model(self):
        """Test that tests/test_models/test_base_model.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_base_model.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_bm_module_docstring(self):
        """Test for the base_model.py module docstring"""
        self.assertIsNot(base_model.__doc__, None,
                         "base_model.py needs a docstring")
        self.assertTrue(len(base_model.__doc__) >= 1,
                        "base_model.py needs a docstring")

    def test_bm_class_docstring(self):
        """Test for the BaseModel class docstring"""
        self.assertIsNot(BaseModel.__doc__, None,
                         "BaseModel class needs a docstring")
        self.assertTrue(len(BaseModel.__doc__) >= 1,
                        "BaseModel class needs a docstring")

    def test_bm_func_docstrings(self):
        """Test for the presence of docstrings in BaseModel methods"""
        for func in self.base_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestBaseModel(unittest.TestCase):
    """Test the BaseModel class"""

    def test_is_base_model(self):
        """test that the instatiation of a BaseModel works"""
        base_model = BaseModel()
        self.assertEqual(type(base_model), BaseModel)

    def test_created_at_instantiation(self):
        """test created_at is a pub. instance attribute of type datetime"""
        base_model = BaseModel()
        self.assertTrue(base_model.created_at is not None)
        self.assertEqual(type(base_model.created_at), datetime)

    def test_updated_at_instantiation(self):
        """test updated_at is a pub. instance attribute of type datetime"""
        base_model = BaseModel()
        self.assertTrue(base_model.updated_at is not None)
        self.assertEqual(type(base_model.updated_at), datetime)

    def test_diff_datetime_objs(self):
        """test that two BaseModel instances have different datetime objects"""
        bm1 = BaseModel()
        bm2 = BaseModel()
        self.assertNotEqual(bm1.created_at, bm2.created_at)
        self.assertNotEqual(bm1.updated_at, bm2.updated_at)

    def test_same_time(self):
        """test updated_at and created_at are the same for a new instance"""
        base_model = BaseModel()
        self.assertEqual(base_model.updated_at, base_model.created_at)

    def test_to_dict(self):
        """Test conversion of object attributes to dictionary for json"""
        my_model = BaseModel()
        my_model.name = "Holberton"
        my_model.my_number = 89
        d = my_model.to_dict()
        expected_attrs = ["id",
                          "created_at",
                          "updated_at",
                          "name",
                          "my_number",
                          "__class__"]
        self.assertCountEqual(d.keys(), expected_attrs)
        self.assertEqual(d['__class__'], 'BaseModel')
        self.assertEqual(d['name'], "Holberton")
        self.assertEqual(d['my_number'], 89)

    def test_date_differences(self):
        """Test use of datetime for `created_at` attribute"""
        my_model = BaseModel()
        now = datetime.now()
        self.assertTrue(type(my_model.created_at) == type(now))
        self.assertTrue(type(my_model.updated_at) == type(now))
        self.assertEqual(my_model.created_at, my_model.updated_at)
        delta = now - my_model.created_at
        self.assertAlmostEqual(delta.total_seconds(), 0.0, delta=1e-2)

    def test_valid_UUID_creation(self):
        '''test created_at is a saloon.'''
        bm = BaseModel()
        id = bm.id
        allhex = id.split('-')
        # id is a string
        self.assertIs(type(id), str)
        # len(id) = 37
        self.assertIs(len(id), 36)
        # dash at 8, 13, 18, 23 indexes
        self.assertIs(id[8], "-")
        self.assertIs(id[13], "-")
        self.assertIs(id[18], "-")
        self.assertIs(id[23], "-")

        # all hex characters between dashes
        for substring in allhex:
            self.assertIs(all(c in string.hexdigits for c in substring), True)

    def test_to_dict_creates_dict(self):
        """test to_dict method creates a dictionary with proper attrs"""
        bm = BaseModel()
        new_d = bm.to_dict()
        self.assertEqual(type(new_d), dict)
        for attr in bm.__dict__:
            self.assertTrue(attr in new_d)
        self.assertTrue("__class__" in new_d)

    def test_to_dict_values(self):
        """test that values in dict returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        bm = BaseModel()
        new_d = bm.to_dict()
        self.assertEqual(new_d["__class__"], "BaseModel")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], bm.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"], bm.updated_at.strftime(t_format))

    def test_str(self):
        """test that the str method has the correct output"""
        bm = BaseModel()
        string = "[BaseModel] ({}) {}".format(bm.id, bm.__dict__)
        self.assertEqual(string, str(bm))
