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
        """Set up for docstring tests"""
        cls.base_funcs = inspect.getmembers(BaseModel, inspect.isfunction)

    def test_pep8_conformance(self):
        """Test that models/base_model.py conforms to PEP8."""
        for path in ['models/base_model.py', 'tests/test_models/test_base_model.py']:
            with self.subTest(path=path):
                errors = pycodestyle.Checker(path).check_all()
                self.assertEqual(errors, 0)

    def test_module_docstring(self):
        """Test for the existence of module docstring"""
        self.assertIsNot(module_doc, None, "base_model.py needs a docstring")
        self.assertTrue(len(module_doc) > 1, "base_model.py needs a docstring")

    def test_class_docstring(self):
        """Test for the BaseModel class docstring"""
        self.assertIsNot(BaseModel.__doc__, None, "BaseModel class needs a docstring")
        self.assertTrue(len(BaseModel.__doc__) >= 1, "BaseModel class needs a docstring")

    def test_func_docstrings(self):
        """Test for the presence of docstrings in BaseModel methods"""
        for func in self.base_funcs:
            with self.subTest(function=func):
                self.assertIsNot(func[1].__doc__, None, "{:s} method needs a docstring".format(func[0]))
                self.assertTrue(len(func[1].__doc__) > 1, "{:s} method needs a docstring".format(func[0]))


class TestBaseModel(unittest.TestCase):
    """Test the BaseModel class"""

    def test_instantiation(self):
        """Test that object is correctly created"""
        inst = BaseModel()
        self.assertIs(type(inst), BaseModel)
        inst.name = "Holberton"
        inst.number = 89
        attrs_types = {"id": str, "created_at": datetime, "updated_at": datetime, "name": str, "number": int}
        for attr, typ in attrs_types.items():
            with self.subTest(attr=attr, typ=typ):
                self.assertIn(attr, inst.__dict__)
                self.assertIs(type(inst.__dict__[attr]), typ)
        self.assertEqual(inst.name, "Holberton")
        self.assertEqual(inst.number, 89)

    def test_datetime_attributes(self):
        """Test that two BaseModel instances have different datetime objects
        and that upon creation have identical updated_at and created_at
        value."""
        inst1 = BaseModel()
        tic = datetime.utcnow()
        inst1.created_at = tic
        toc = datetime.utcnow()
        self.assertTrue(tic <= inst1.created_at <= toc)
        time.sleep(1e-4)
        inst2 = BaseModel()
        tic = datetime.utcnow()
        inst2.created_at = tic
        toc = datetime.utcnow()
        self.assertTrue(tic <= inst2.created_at <= toc)
        self.assertEqual(inst1.created_at, inst1.updated_at)
        self.assertEqual(inst2.created_at, inst2.updated_at)
        self.assertNotEqual(inst1.created_at, inst2.created_at)
        self.assertNotEqual(inst1.updated_at, inst2.updated_at)

    def test_uuid(self):
        """Test that id is a valid uuid"""
        inst1 = BaseModel()
        inst2 = BaseModel()
        for inst in [inst1, inst2]:
            uuid = inst.id
            with self.subTest(uuid=uuid):
                self.assertIs(type(uuid), str)
                self.assertRegex(uuid, "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")
        self.assertNotEqual(inst1.id, inst2.id)

    def test_to_dict(self):
        """Test conversion of object attributes to dictionary for JSON"""
        my_model = BaseModel()
        my_model.name = "Holberton"
        my_model.my_number = 89
        d = my_model.to_dict()
        expected_attrs = ["id", "created_at", "updated_at", "name", "my_number", "__class__"]
        self.assertCountEqual(d.keys(), expected_attrs)
        self.assertEqual(d["__class__"], "BaseModel")
        self.assertEqual(d["name"], "Holberton")
        self.assertEqual(d["my_number"], 89)
        self.assertIs(type(d["created_at"]), str)
        self.assertIs(type(d["updatedat"]), str)

    def test_str(self):
        """Test the __str__ method of BaseModel"""
        inst = BaseModel()
        inst.name = "Holberton"
        inst.number = 89
        expected_str = "[BaseModel] ({}) {}".format(inst.id, inst.__dict__)
        self.assertEqual(str(inst), expected_str)

    @mock.patch('models.storage')
    def test_save(self, mock_storage):
        """Test the save method of BaseModel"""
        inst = BaseModel()
        inst.save()
        self.assertNotEqual(inst.created_at, inst.updated_at)
        self.assertTrue(mock_storage.save.called)

    def test_create_with_dict(self):
        """Test creating an instance of BaseModel with a dictionary"""
        my_dict = {
            'id': '123',
            'created_at': '2022-01-01T00:00:00',
            'updated_at': '2022-01-01T00:00:00',
            '__class__': 'BaseModel',
            'name': 'Holberton',
            'number': 89
        }
        inst = BaseModel(**my_dict)
        self.assertEqual(inst.id, '123')
        self.assertEqual(inst.created_at, datetime(2022, 1, 1, 0, 0, 0))
        self.assertEqual(inst.updated_at, datetime(2022, 1, 1, 0, 0, 0))
        self.assertEqual(inst.name, 'Holberton')
        self.assertEqual(inst.number, 89)

    def test_create_with_dict_missing_attributes(self):
        """Test creating an instance of BaseModel with a dictionary
        missing some attributes"""
        my_dict = {
            'id': '123',
            'created_at': '2022-01-01T00:00:00',
            '__class__': 'BaseModel',
            'name': 'Holberton',
        }
        inst = BaseModel(**my_dict)
        self.assertEqual(inst.id, '123')
        self.assertEqual(inst.created_at, datetime(2022, 1, 1, 0, 0, 0))
        self.assertEqual(inst.updated_at, inst.created_at)
        self.assertEqual(inst.name, 'Holberton')
        self.assertFalse(hasattr(inst, 'number'))

    def test_create_with_dict_extra_attributes(self):
        """Test creating an instance of BaseModel with a dictionary
        containing extra attributes"""
        my_dict = {
            'id': '123',
            'created_at': '2022-01-01T00:00:00',
            'updated_at': '2022-01-01T00:00:00',
            '__class__': 'BaseModel',
            'name': 'Holberton',
            'number': 89,
            'extra': 'attribute'
        }
        inst = BaseModel(**my_dict)
        self.assertEqual(inst.id, '123')
        self.assertEqual(inst.created_at, datetime(2022, 1, 1, 0, 0, 0))
        self.assertEqual(inst.updated_at, datetime(2022, 1, 1, 0, 0, 0))
        self.assertEqual(inst.name, 'Holberton')
        self.assertEqual(inst.number, 89)
        self.assertFalse(hasattr(inst, 'extra'))


if __name__ == "__main__":
    unittest.main()
