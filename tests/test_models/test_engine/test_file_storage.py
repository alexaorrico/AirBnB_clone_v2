#!/usr/bin/python3
"""test for file storage"""
import unittest
from datetime import datetime
import inspect
import pep8
import json
import os
from models import engine
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.file_storage import FileStorage


class TestFileStorage(unittest.TestCase):
    '''this will test the FileStorage'''

    @classmethod
    def setUpClass(cls):
        """set up for test"""
        cls.user = User()
        cls.user.first_name = "Kev"
        cls.user.last_name = "Yo"
        cls.user.email = "1234@yahoo.com"
        cls.storage = FileStorage()

    @classmethod
    def teardown(cls):
        """at the end of the test this will tear it down"""
        del cls.user

    def tearDown(self):
        """teardown"""
        try:
            os.remove("file.json")
        except Exception:
            pass

    def test_pep8_FileStorage(self):
        """Tests pep8 style"""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(['models/engine/file_storage.py'])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_all(self):
        """tests if all works in File Storage"""
        storage = FileStorage()
        obj = storage.all()
        self.assertIsNotNone(obj)
        self.assertEqual(type(obj), dict)
        self.assertIs(obj, storage._FileStorage__objects)

    def test_all_v2(self):
        """Tests the new all() method in the v2"""
        storage = FileStorage()
        users = storage.all(User)
        self.assertIsNotNone(users)
        self.assertEqual(type(users), dict)

    def test_new(self):
        """test when new is created"""
        storage = FileStorage()
        obj = storage.all()
        user = User()
        user.id = 123455
        user.name = "Kevin"
        storage.new(user)
        key = user.__class__.__name__ + "." + str(user.id)
        self.assertIsNotNone(obj[key])

    def test_reload_filestorage(self):
        """Tests reload"""
        self.storage.save()
        Root = os.path.dirname(os.path.abspath("console.py"))
        path = os.path.join(Root, "file.json")
        with open(path, 'r') as f:
            lines = f.readlines()
        try:
            os.remove(path)
        except:
            pass
        self.storage.save()
        with open(path, 'r') as f:
            lines2 = f.readlines()
        self.assertEqual(lines, lines2)
        try:
            os.remove(path)
        except:
            pass
        with open(path, "w") as f:
            f.write("{}")
        with open(path, "r") as r:
            for line in r:
                self.assertEqual(line, "{}")
        self.assertIs(self.storage.reload(), None)

    def test_delete(self):
        """Tests the delete v2 method"""
        storage = FileStorage()
        new_state = State()
        new_state.name = "California"
        storage.new(new_state)
        storage.save()
        states = storage.all(State)
        self.assertIsNotNone(states)
        self.assertEqual(type(states), dict)
        storage.delete(new_state)
        states = storage.all(State)
        self.assertEqual(states, {})

    def test_count_cls(self):
        """... checks count method with class input arg"""
        count_user = storage.count('User')
        expected = 1
        self.assertEqual(expected, count_user)

    def test_count_all(self):
        """... checks the count method with no class input"""
        count_all = storage.count()
        expected = 2
        self.assertEqual(expected, count_all)

    def test_get_cls_id(self):
        """... checks get method with class and id inputs"""
        duplicate = storage.get('User', self.user.id)
        expected = self.user.id
        actual = duplicate.id
        self.assertEqual(expected, actual)

    def test_all(self):
        """... checks if all() function returns newly created instance"""
        u_id = self.user.id
        all_obj = storage.all()
        actual = False
        for k in all_obj.keys():
            if u_id in k:
                actual = True
        self.assertTrue(actual)

    def test_obj_saved_to_file(self):
        """... checks proper FileStorage instantiation"""
        remove(F)
        self.user.save()
        u_id = self.user.id
        actual = False
        with open(F, mode='r', encoding='utf-8') as f_obj:
            storage_dict = json.load(f_obj)
        for k in storage_dict.keys():
            if u_id in k:
                actual = True
        self.assertTrue(actual)

    def test_reload(self):
        """... checks proper usage of reload function"""
        remove(F)
        self.bm_obj.save()
        u_id = self.bm_obj.id
        actual = False
        new_storage = FileStorage()
        new_storage.reload()
        all_obj = new_storage.all()
        for k in all_obj.keys():
            if u_id in k:
                actual = True
        self.assertTrue(actual)


if __name__ == "__main__":
    unittest.main()
