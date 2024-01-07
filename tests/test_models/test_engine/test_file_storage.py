#!/usr/bin/python3
"""
Unit Test for BaseModel Class
"""
import unittest
from datetime import datetime
import models
from models import engine
from models.engine.file_storage import FileStorage
import json
import os

User = models.user.User
BaseModel = models.base_model.BaseModel
FileStorage = engine.file_storage.FileStorage
storage = models.storage
F = './dev/file.json'
storage_type = os.environ.get('HBNB_TYPE_STORAGE')


@unittest.skipIf(storage_type == 'db', 'skip if environ is db')
class TestFileStorageDocs(unittest.TestCase):
    """Class for testing BaseModel docs"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('..... Testing Documentation .....')
        print('..... For FileStorage Class .....')
        print('.................................\n\n')

    def test_doc_file(self):
        """... documentation for the file"""
        expected = ("\nHandles I/O, writing and reading, of JSON for storage "
                    "of all class instances\n")
        actual = models.file_storage.__doc__
        self.assertEqual(expected, actual)

    def test_doc_class(self):
        """... documentation for the class"""
        expected = 'handles long term storage of all class instances'
        actual = FileStorage.__doc__
        self.assertEqual(expected, actual)

    def test_doc_all(self):
        """... documentation for all function"""
        expected = 'returns private attribute: __objects'
        actual = FileStorage.all.__doc__
        self.assertEqual(expected, actual)

    def test_doc_new(self):
        """... documentation for new function"""
        expected = ("sets / updates in __objects the obj with key <obj class "
                    "name>.id")
        actual = FileStorage.new.__doc__
        self.assertEqual(expected, actual)

    def test_doc_save(self):
        """... documentation for save function"""
        expected = 'serializes __objects to the JSON file (path: __file_path)'
        actual = FileStorage.save.__doc__
        self.assertEqual(expected, actual)

    def test_doc_reload(self):
        """... documentation for reload function"""
        expected = ("if file exists, deserializes JSON file to __objects, "
                    "else nothing")
        actual = FileStorage.reload.__doc__
        self.assertEqual(expected, actual)

    def test_doc_get(self):
        """... documentation for get function"""
        expected = "\n            a method to retrieve one object"
        expected += "\n            cls: string representating the class name"
        expected += "\n            id: string representating the object ID"
        expected += "\n        "
        actual = FileStorage.get.__doc__
        self.assertEqual(expected, actual)

    def test_doc_count(self):
        """... documentation for count function"""
        expected = "\n            a method to count the number of objects in "
        expected += "storage\n            cls: string representing the class "
        expected += "name\n        "
        actual = FileStorage.count.__doc__
        self.assertEqual(expected, actual)


@unittest.skipIf(storage_type == 'db', 'skip if environ is db')
class TestBmFsInstances(unittest.TestCase):
    """testing for class instances"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('...... Testing FileStorate ......')
        print('..... For FileStorage Class .....')
        print('.................................\n\n')

    def setUp(self):
        """initializes new storage object for testing"""
        self.storage = FileStorage()
        self.bm_obj = BaseModel()

    def test_instantiation(self):
        """... checks proper FileStorage instantiation"""
        self.assertIsInstance(self.storage, FileStorage)

    def test_storage_file_exists(self):
        """... checks proper FileStorage instantiation"""
        os.remove(F)
        self.bm_obj.save()
        self.assertTrue(os.path.isfile(F))

    def test_obj_saved_to_file(self):
        """... checks proper FileStorage instantiation"""
        os.remove(F)
        self.bm_obj.save()
        bm_id = self.bm_obj.id
        actual = 0
        with open(F, mode='r', encoding='utf-8') as f_obj:
            storage_dict = json.load(f_obj)
        for k in storage_dict.keys():
            if bm_id in k:
                actual = 1
        self.assertTrue(1 == actual)

    def test_to_json(self):
        """... to_json should return serializable dict object"""
        my_model_json = self.bm_obj.to_json()
        actual = 1
        try:
            serialized = json.dumps(my_model_json)
        except:
            actual = 0
        self.assertTrue(1 == actual)

    def test_reload(self):
        """... checks proper usage of reload function"""
        os.remove(F)
        self.bm_obj.save()
        bm_id = self.bm_obj.id
        actual = 0
        new_storage = FileStorage()
        new_storage.reload()
        all_obj = new_storage.all()
        for k in all_obj.keys():
            if bm_id in k:
                actual = 1
        self.assertTrue(1 == actual)

    def test_save_reload_class(self):
        """... checks proper usage of class attribute in file storage"""
        os.remove(F)
        self.bm_obj.save()
        bm_id = self.bm_obj.id
        actual = 0
        new_storage = FileStorage()
        new_storage.reload()
        all_obj = new_storage.all()
        for k, v in all_obj.items():
            if bm_id in k:
                if type(v).__name__ == 'BaseModel':
                    actual = 1
        self.assertTrue(1 == actual)

    def test_bm_get(self):
        """... checks if get() works with BaseModel"""
        test_class = self.bm_obj.__class__.__name__
        test_id = self.bm_obj.id
        test_obj = self.bm_obj
        result_get = storage.get(test_class, test_id)
        self.assertTrue(test_obj, result_get)

    def test_db_count(self):
        """...checks if count() works with BaseModel"""
        first_count = storage.count('BaseModel')
        self.bm_obj2 = BaseModel()
        self.bm_obj2.save()
        second_count = storage.count('BaseModel')
        self.assertTrue(first_count + 1, second_count)


@unittest.skipIf(storage_type == 'db', 'skip if environ is db')
class TestUserFsInstances(unittest.TestCase):
    """testing for class instances"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('...... Testing FileStorage ......')
        print('.......... User  Class ..........')
        print('.................................\n\n')

    def setUp(self):
        """initializes new user for testing"""
        self.user = User()
        self.bm_obj = BaseModel()

#    @unittest.skipIf(storage_type == 'db', 'skip if environ is db')
    def test_storage_file_exists(self):
        """... checks proper FileStorage instantiation"""
        os.remove(F)
        self.user.save()
        self.assertTrue(os.path.isfile(F))

#    @unittest.skipIf(storage_type == 'db', 'skip if environ is db')
    def test_obj_saved_to_file(self):
        """... checks proper FileStorage instantiation"""
        os.remove(F)
        self.user.save()
        u_id = self.user.id
        actual = 0
        with open(F, mode='r', encoding='utf-8') as f_obj:
            storage_dict = json.load(f_obj)
        for k in storage_dict.keys():
            if u_id in k:
                actual = 1
        self.assertTrue(1 == actual)

#    @unittest.skipIf(storage_type == 'db', 'skip if environ is db')
    def test_reload(self):
        """... checks proper usage of reload function"""
        os.remove(F)
        self.bm_obj.save()
        u_id = self.bm_obj.id
        actual = 0
        new_storage = FileStorage()
        new_storage.reload()
        all_obj = new_storage.all()
        for k in all_obj.keys():
            if u_id in k:
                actual = 1
        self.assertTrue(1 == actual)


if __name__ == '__main__':
    unittest.main