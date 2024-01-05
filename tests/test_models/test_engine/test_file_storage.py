#!/usr/bin/python3
'''
    The file_storage module is being tested.
'''

import os
import time
import json
import unittest
import models
from models import storage
from models.base_model import BaseModel
from models.state import State
from models.engine.file_storage import FileStorage

db = os.getenv("HBNB_TYPE_STORAGE")


@unittest.skipIf(db == 'db', "Testing DBstorage only")
class testFileStorage(unittest.TestCase):
    '''
        Putting the FileStorage class to the test.
    '''

    def setUp(self):
        '''
            Class initialization
        '''
        self.storage = FileStorage()
        self.my_model = BaseModel()

    def tearDown(self):
        '''
            Cleaning is being done.
        '''

        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_all_return_type(self):
        '''
            Validates data type of all method and return value.
        '''
        storage_all = self.storage.all()
        self.assertIsInstance(storage_all, dict)

    def test_new_method(self):
        '''
            Sets correct key and pair in FileStorage.__object attribute.
        '''
        self.storage.new(self.my_model)
        key = str(self.my_model.__class__.__name__ + "." + self.my_model.id)
        self.assertTrue(key in self.storage._FileStorage__objects)

    def test_objects_value_type(self):
        '''
            Value stored in FileStorage.__object is obj.__class__.__name__.
        '''
        self.storage.new(self.my_model)
        key = str(self.my_model.__class__.__name__ + "." + self.my_model.id)
        val = self.storage._FileStorage__objects[key]
        self.assertIsInstance(self.my_model, type(val))

    def test_save_file_exists(self):
        '''
            Ensures that a file with the name file is created.json
        '''
        self.storage.save()
        self.assertTrue(os.path.isfile("file.json"))

    def test_save_file_read(self):
        '''
            Examining contents of files contained within the file.json
        '''
        self.storage.save()
        self.storage.new(self.my_model)

        with open("file.json", encoding="UTF8") as fd:
            content = json.load(fd)

        self.assertTrue(type(content) is dict)

    def test_the_type_file_content(self):
        '''
            Examining the kind of information contained in the file.
        '''
        self.storage.save()
        self.storage.new(self.my_model)

        with open("file.json", encoding="UTF8") as fd:
            content = fd.read()

        self.assertIsInstance(content, str)

    def test_reaload_without_file(self):
        '''
            Nothing occurs upon file.JSON is not present.
        '''

        try:
            self.storage.reload()
            self.assertTrue(True)
        except:
            self.assertTrue(False)

    def test_delete(self):
        '''
            Test the remove technique.
        '''
        fs = FileStorage()
        new_state = State()
        fs.new(new_state)
        state_id = new_state.id
        fs.save()
        fs.delete(new_state)
        with open("file.json", encoding="UTF-8") as fd:
            state_dict = json.load(fd)
        for k, v in state_dict.items():
            self.assertFalse(state_id == k.split('.')[1])

    def test_model_storage(self):
        '''
            Check the Filestorage tests State Model
        '''
        self.assertTrue(isinstance(storage, FileStorage))

    def test_get(self):
        '''
            Check that method returns the requested object.
        '''
        new_state = State(name="NewYork")
        storage.new(new_state)
        key = "State.{}".format(new_state.id)
        result = storage.get("State", new_state.id)
        self.assertTrue(result.id, new_state.id)
        self.assertIsInstance(result, State)

    def test_count(self):
        '''
            Verify that count method yields number of items.
        '''
        old_count = storage.count("State")
        new_state1 = State(name="NewYork")
        storage.new(new_state1)
        new_state2 = State(name="Virginia")
        storage.new(new_state2)
        new_state3 = State(name="California")
        storage.new(new_state3)
        self.assertEqual(old_count + 3, storage.count("State"))
