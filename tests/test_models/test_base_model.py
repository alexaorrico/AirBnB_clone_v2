#!/usr/bin/python3
"""Test BaseModel for expected behavior and documentation"""
from datetime import datetime
import inspect
import models
import pep8 as pycodestyle
import time
import unittest
from unittest import mock

BaseModel = models.base_model.BaseModel
module_doc = models.base_model.__doc__


class TestBaseModelDocs(unittest.TestCase):
    """Tests to check the documentation and style of BaseModel class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.base_funcs = inspect.getmembers(BaseModel, inspect.isfunction)

    def test_pep8_conformance_base_model(self):
        """Test that models/base_model.py conforms to PEP8."""
        for path in [
            "models/base_model.py",
            "tests/test_models/test_base_model.py",
        ]:
            style = pycodestyle.StyleGuide(quiet=True)
            result = style.check_files([path])
            self.assertEqual(
                result.total_errors,
                0,
                "Found code style errors (and warnings).",
            )

    def test_module_docstring(self):
        """Test for the existence of module docstring"""
        self.assertTrue(len(module_doc) > 0)

    def test_class_docstring(self):
        """Test for the BaseModel class docstring"""
        self.assertTrue(len(BaseModel.__doc__) > 0)

    def test_functions_docstrings(self):
        """Test for the presence of docstrings in BaseModel methods"""
        for func in self.base_funcs:
            self.assertTrue(len(func[1].__doc__) > 0)


class TestBaseModel(unittest.TestCase):
    """Test the BaseModel class"""

    def test_is_subclass(self):
        """Test that BaseModel is a subclass of object"""
        base = BaseModel()
        self.assertIsInstance(base, object)

    def test_id(self):
        """Test that id is an instance of string"""
        base = BaseModel()
        self.assertIsInstance(base.id, str)

    def test_created_at(self):
        """Test that created_at is an instance of datetime"""
        base = BaseModel()
        self.assertIsInstance(base.created_at, datetime)

    def test_updated_at(self):
        """Test that updated_at is an instance of datetime"""
        base = BaseModel()
        self.assertIsInstance(base.updated_at, datetime)

    def test_save(self):
        """Test the save method"""
        base = BaseModel()
        old_time = base.updated_at
        time.sleep(0.1)
        base.save()
        self.assertNotEqual(old_time, base.updated_at)

    def test_to_dict(self):
        """Test the to_dict method"""
        base = BaseModel()
        base_dict = base.to_dict()
        self.assertIsInstance(base_dict, dict)
        for key in base_dict:
            self.assertTrue(
                key
                in [
                    "id",
                    "created_at",
                    "updated_at",
                    "__class__",
                ]
            )
        self.assertEqual(base_dict["__class__"], "BaseModel")
        self.assertEqual(base_dict["id"], base.id)

    def test_str(self):
        """Test the str method"""
        base = BaseModel()
        self.assertEqual(
            str(base), "[BaseModel] ({}) {}".format(base.id, base.__dict__)
        )

    def test_kwargs(self):
        """Test the kwargs argument"""
        base = BaseModel()
        base.name = "Holberton"
        base.my_number = 89
        base_dict = base.to_dict()
        new_base = BaseModel(**base_dict)
        self.assertEqual(base.id, new_base.id)
        self.assertEqual(base.created_at, new_base.created_at)
        self.assertEqual(base.updated_at, new_base.updated_at)
        self.assertEqual(base.name, new_base.name)
        self.assertEqual(base.my_number, new_base.my_number)

    def test_instance(self):
        """Test the instance argument"""
        base = BaseModel()
        self.assertIsInstance(base, BaseModel)

    def test_save_with_arg(self):
        """Test the save method with an argument"""
        base = BaseModel()
        with mock.patch("models.storage") as mock_storage:
            base.save("Hello")
        self.assertEqual(base.save("Hello"), None)
        self.assertTrue(mock_storage.save.called)
        self.assertEqual(mock_storage.save.call_count, 1)
