#!/usr/bin/python3
""" Module for testing file storage"""
import models
import unittest
from models.base_model import BaseModel
from models import storage
import os
from models.engine import file_storage
from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage
from models.state import State


class test_fileStorage(unittest.TestCase):
    """ Class to test the file storage method """

    @unittest.skipIf(type(models.storage) == DBStorage,
                     "Testing DBStorage")
    def setUp(self):
        """ Set up test environment """
        del_list = []
        self.storage = FileStorage()
        for key in self.storage.all().keys():
            del_list.append(key)
        for key in del_list:
            del self.storage.all()[key]

    @unittest.skipIf(type(models.storage) == DBStorage,
                     "Testing DBStorage")
    def tearDown(self):
        """ Remove storage file at end of tests """
        try:
            os.remove('file.json')
        except:
            pass

    @unittest.skipIf(type(models.storage) == DBStorage,
                     "Testing DBStorage")
    def test_obj_list_empty(self):
        """ __objects is initially empty """
        self.assertEqual(len(storage.all()), 0)

    @unittest.skipIf(type(models.storage) == DBStorage,
                     "Testing DBStorage")
    def test_new(self):
        """ New object is correctly added to __objects """
        new = BaseModel()
        new.save()
        self.assertEqual(new in storage.all().values(), True)

    @unittest.skipIf(type(models.storage) == DBStorage,
                     "Testing DBStorage")
    def test_all(self):
        """ __objects is properly returned """
        new = BaseModel()
        temp = self.storage.all()
        self.assertIsInstance(temp, dict)

    @unittest.skipIf(type(models.storage) == DBStorage,
                     "Testing DBStorage")
    def test_base_model_instantiation(self):
        """ File is not created on BaseModel save """
        new = BaseModel()
        self.assertFalse(os.path.exists('file.json'))

    @unittest.skipIf(type(models.storage) == DBStorage,
                     "Testing DBStorage")
    def test_empty(self):
        """ Data is saved to file """
        new = BaseModel()
        thing = new.to_dict()
        self.storage.new(new)
        self.storage.save()
        new2 = BaseModel(**thing)
        self.assertNotEqual(os.path.getsize('file.json'), 0)

    @unittest.skipIf(type(models.storage) == DBStorage,
                     "Testing DBStorage")
    def test_save(self):
        """ FileStorage save method """
        new = BaseModel()
        self.storage.save()
        self.assertTrue(os.path.exists('file.json'))

    @unittest.skipIf(type(models.storage) == DBStorage,
                     "Testing DBStorage")
    def test_reload(self):
        """ Storage file is successfully loaded to __objects """
        new = BaseModel()
        storage.save()
        storage.reload()
        for obj in self.storage.all().values():
            loaded = obj
            self.assertEqual(new.to_dict()['id'], loaded.to_dict()['id'])

    @unittest.skipIf(type(models.storage) == DBStorage,
                     "Testing DBStorage")
    def test_reload_from_nonexistent(self):
        """ Nothing happens if file does not exist """
        self.assertEqual(storage.reload(), None)

    @unittest.skipIf(type(models.storage) == DBStorage,
                     "Testing DBStorage")
    def test_base_model_save(self):
        """ BaseModel save method calls storage save """
        new = BaseModel()
        self.storage.new(new)
        self.storage.save()
        self.assertTrue(os.path.exists('file.json'))

    """def test_type_path(self):
        " Confirm __file_path is string "
        self.assertEqual(type(storage._FileStorage__file_path), str)"""

    @unittest.skipIf(type(models.storage) == DBStorage,
                     "Testing DBStorage")
    def test_type_objects(self):
        """ Confirm __objects is a dict """
        self.assertEqual(type(self.storage.all()), dict)

    @unittest.skipIf(type(models.storage) == DBStorage,
                     "Testing DBStorage")
    def test_key_format(self):
        """ Key is properly formatted """
        new = BaseModel()
        _id = new.to_dict()['id']
        for key in self.storage.all().keys():
            temp = key
            self.assertEqual(temp, 'BaseModel' + '.' + _id)

    @unittest.skipIf(type(models.storage) == DBStorage,
                     "Testing DBStorage")
    def test_storage_var_created(self):
        """ FileStorage object storage created """
        from models.engine.file_storage import FileStorage
        print(type(self.storage))
        self.assertEqual(type(self.storage), FileStorage)

    @unittest.skipIf(type(models.storage) == DBStorage,
                     "Testing DBStorage")
    def test_documentation(self):
        """ Test docstrings documentation"""

        self.assertTrue(file_storage.__doc__)
        self.assertTrue(file_storage.FileStorage.__doc__)

    @unittest.skipIf(type(models.storage) == DBStorage,
                     "Testing DBStorage")
    def test_methods_doc(self):
        """ Test all docstrings of each method"""

        for all_methods in dir(FileStorage):
            self.assertTrue(all_methods.__doc__)

    @unittest.skipIf(models.storage_t == DBStorage, "Testing DBStorage")
    def test_get(self):
        state = State(name='Albania')
        state.save()
        x = self.storage.get(State, state.id)
        self.assertEqual(x, state)

    @unittest.skipIf(models.storage_t == DBStorage, "Testing DBStorage")
    def test_count(self):
        state = State(name='another')
        state.save()
        self.assertEqual(len(self.storage.all()), storage.count())
        self.assertEqual(len(self.storage.all(State)), storage.count(State))


if __name__ == '__main__':
    unittest.main()
