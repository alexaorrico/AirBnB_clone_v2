#!/usr/bin/python3
"""test for file storage"""
import unittest
from holbertonschool-higher_level_programming.python-input_output.8-main_2 import MyClass
import pep8
import os
from models.user import User
from models.state import State
from models.engine.file_storage import FileStorage
from models import storage


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
        """
        tests reload
        """
        self.storage.save()
        Root = os.path.dirname(os.path.abspath("console.py"))
        path = os.path.join(Root, "file.json")
        with open(path, 'r') as f:
            lines = f.readlines()
        try:
            os.remove(path)
        except KeyError:
            pass
        self.storage.save()
        with open(path, 'r') as f:
            lines2 = f.readlines()
        self.assertEqual(lines, lines2)
        try:
            os.remove(path)
        except IndexError:
            pass
        with open(path, "w") as f:
            f.write("{}")
        with open(path, "r") as r:
            for line in r:
                self.assertEqual(line, "{}")
        self.assertIs(self.storage.reload(), None)

    def setUp(self):
        self.file_storage = storage.FileStorage()
        self.file_storage.reload()

    def tearDown(self):
        self.file_storage.close()

    def test_get_existing_object(self):
        """Test retrieving an existing object using get()"""
        new_state = State(name="California")
        storage.new(new_state)
        storage.save()

        retrieved_state = self.file_storage.get(State, new_state.id)
        self.assertEqual(retrieved_state, new_state)

    def test_get_positive():
        """Create object and add to storage."""

        obj = MyClass()
        storage.add(obj)
    # retrieve object and verify correct object is returned
        assert storage.get(MyClass, obj.id) == obj

    def test_get_negative():
        # attempt to retrieve object that does not exist in storage
        assert storage.get(MyClass, "nonexistent_id") == None

    def test_count_positive():
        # create objects and add to storage
        obj1 = MyClass()
        obj2 = MyClass()
        obj3 = OtherClass()
        storage.add(obj1)
        storage.add(obj2)
        storage.add(obj3)
    # count objects for MyClass and verify count is correct
        assert storage.count(MyClass) == 2

    def test_count_negative():
        # count objects for class that does not exist
        assert storage.count(NonexistentClass) == 0


if __name__ == "__main__":
    unittest.main()
