#!/usr/bin/python3
"""Test BaseModel for expected behavior and documentation"""
from datetime import datetime
import inspect
import models
import pep8
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
        cls.base_funcs = inspect.getmembers(
            BaseModel, inspect.isfunction)

    def test_pep8_conformance(self):
        """Test that models/base_model.py conforms to PEP8."""
        paths = [
            'models/base_model.py',
            'tests/test_models/test_base_model.py']
        for path in paths:
            with self.subTest(path=path):
                style = pep8.StyleGuide()
                result = style.check_files([path])
                self.assertEqual(
                        result.total_errors, 0,
                        "PEP8 style violations found in {}".format(path))

    def test_module_docstring(self):
        """Test for the existence of module docstring"""
        self.assertIsNot(module_doc, None,
                         "base_model.py needs a docstring")
        self.assertTrue(len(module_doc) > 1,
                        "base_model.py needs a docstring")

    def test_class_docstring(self):
        """Test for the BaseModel class docstring"""
        self.assertIsNot(BaseModel.__doc__, None,
                         "BaseModel class needs a docstring")
        self.assertTrue(len(BaseModel.__doc__) >= 1,
                        "BaseModel class needs a docstring")

    def test_func_docstrings(self):
        """Test for the presence of docstrings in BaseModel methods"""
        for func in self.base_funcs:
            with self.subTest(function=func):
                self.assertIsNot(
                    func[1].__doc__,
                    None,
                    "{:s} method needs a docstring".format(func[0])
                )
                self.assertTrue(
                    len(func[1].__doc__) > 1,
                    "{:s} method needs a docstring".format(func[0])
                )


class TestBaseModel(unittest.TestCase):
    """Test the BaseModel class"""

    def test_instantiation(self):
        """Test that object is correctly created"""
        inst = BaseModel()
        self.assertIs(type(inst), BaseModel)
        inst.name = "Holberton"
        inst.number = 89
        attrs_types = {
            "id": str,
            "created_at": datetime,
            "updated_at": datetime,
            "name": str,
            "number": int
        }
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
        time.sleep(0.1)
        inst2 = BaseModel()
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
                self.assertRegex(uuid,
                                 '^[0-9a-f]{8}-[0-9a-f]{4}'
                                 '-[0-9a-f]{4}-[0-9a-f]{4}'
                                 '-[0-9a-f]{12}$')
        self.assertNotEqual(inst1.id, inst2.id)

    def test_to_dict(self):
        """Test conversion of object attributes to dictionary for json"""
        my_model = BaseModel()
        expected_attrs = ["id",
                          "created_at",
                          "updated_at",
                          "__class__"]
        d = my_model.to_dict()
        self.assertEqual(set(d.keys()), set(expected_attrs))

    def test_to_dict_values(self):
        """test that values in dict returned from to_dict are correct"""
        bm = BaseModel()
        new_d = bm.to_dict()

        # Ensure '__class__' is present and has the correct value
        self.assertEqual(new_d.get("__class__"), "BaseModel")

        # Ensure 'created_at' and 'updated_at' are present and are strings
        self.assertTrue(isinstance(new_d.get("created_at"), str))
        self.assertTrue(isinstance(new_d.get("updated_at"), str))

        # If 'created_at' and 'updated_at' are present, ensure they match the
        # expected format
        created_at_str = new_d.get("created_at")
        updated_at_str = new_d.get("updated_at")
        if created_at_str and updated_at_str:
            t_format = "%Y-%m-%dT%H:%M:%S.%f"
            created_at = datetime.strptime(created_at_str, t_format)
            updated_at = datetime.strptime(updated_at_str, t_format)
            self.assertEqual(created_at, bm.created_at)
            self.assertEqual(updated_at, bm.updated_at)

    def test_str(self):
        """test that the str method has the correct output"""
        inst = BaseModel()
        string = "[BaseModel] ({}) {}".format(inst.id, inst.__dict__)
        self.assertEqual(string, str(inst))

    @mock.patch('models.storage')
    def test_save(self, mock_storage):
        """Test that save method updates `updated_at` and calls
        `storage.save`"""
        inst = BaseModel()
        old_created_at = inst.created_at
        old_updated_at = inst.updated_at
        inst.save()
        new_created_at = inst.created_at
        new_updated_at = inst.updated_at
        self.assertNotEqual(old_updated_at, new_updated_at)
        self.assertEqual(old_created_at, new_created_at)
        self.assertTrue(mock_storage.new.called)
        self.assertTrue(mock_storage.save.called)

    @mock.patch('models.storage')
    def test_delete(self, mock_storage):
        """Test that delete method deletes the instance"""
        inst = BaseModel()
        #   models.storage.new(inst)
        #   models.storage.save()
        #   inst_id = inst.id
        inst.delete()
        #   models.storage.delete(inst)
        #   self.assertNotEqual(models.storage.get(BaseModel, inst_id), None)
        #   self.assertIsNone(models.storage.get(BaseModel, inst_id))
        mock_storage.delete.assert_called_with(inst)

    def test_to_dict_exclude(self):
        """Test that certain attributes are excluded from the to_dict method"""
        obj = BaseModel()
        inst_dict = obj.to_dict()
        #   excluded_attrs = ["__class__", "created_at", "updated_at"]
        excluded_attrs = ['_sa_instance_state']
        #   inst_dict = inst.to_dict()
        for attr in excluded_attrs:
            # with self.subTest(attr=attr):
            self.assertNotIn(attr, inst_dict)
