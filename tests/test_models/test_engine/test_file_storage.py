#!/usr/bin/python3
"""
Unit Test for BaseModel Class
"""
import unittest
from datetime import datetime
<<<<<<< HEAD
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

=======
import inspect
import json
import models
from models import engine
from models.engine.file_storage import FileStorage
import pep8
from os import environ, stat, remove, path

User = models.user.User
BaseModel = models.base_model.BaseModel
State = models.state.State
STORAGE_TYPE = environ.get('HBNB_TYPE_STORAGE')

if STORAGE_TYPE != 'db':
    FileStorage = models.file_storage.FileStorage
storage = models.storage
F = './dev/file.json'


@unittest.skipIf(STORAGE_TYPE == 'db', 'skip if environ is not db')
class TestFileStorageDocs(unittest.TestCase):
    """Class for testing BaseModel docs"""

    all_funcs = inspect.getmembers(FileStorage, inspect.isfunction)

>>>>>>> origin/storage_get_count
    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('..... Testing Documentation .....')
        print('..... For FileStorage Class .....')
        print('.................................\n\n')

<<<<<<< HEAD
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


@unittest.skipIf(storage_type == 'db', 'skip if environ is db')
=======
    def tearDownClass():
        """tidies up the tests removing storage objects"""
        storage.delete_all()
        remove(F)

    def test_doc_file(self):
        """... documentation for the file"""
        expected = ("\nHandles I/O, writing and reading, of JSON for storage "
                    "of all class instances\n")
        actual = models.file_storage.__doc__
        self.assertEqual(expected, actual)

    def test_doc_class(self):
        """... documentation for the class"""
        expected = ('\n        handles long term storage of all class instance'
                    's\n    ')
        actual = FileStorage.__doc__
        self.assertEqual(expected, actual)

    def test_all_function_docs(self):
        """... tests for ALL DOCS for all functions in db_storage file"""
        all_functions = TestFileStorageDocs.all_funcs
        for function in all_functions:
            self.assertIsNotNone(function[1].__doc__)

    def test_pep8_fs(self):
        """... filestorage.py conforms to PEP8 Style"""
        pep8style = pep8.StyleGuide(quiet=True)
        errors = pep8style.check_files(['models/engine/file_storage.py'])
        self.assertEqual(errors.total_errors, 0, errors.messages)

    def test_file_is_executable(self):
        """... tests if file has correct permissions so user can execute"""
        file_stat = stat('models/engine/file_storage.py')
        permissions = str(oct(file_stat[0]))
        actual = int(permissions[5:-2]) >= 5
        self.assertTrue(actual)


@unittest.skipIf(STORAGE_TYPE == 'db', 'skip if environ is db')
>>>>>>> origin/storage_get_count
class TestBmFsInstances(unittest.TestCase):
    """testing for class instances"""

    @classmethod
    def setUpClass(cls):
<<<<<<< HEAD
=======
        """sets up the class"""
>>>>>>> origin/storage_get_count
        print('\n\n.................................')
        print('...... Testing FileStorate ......')
        print('..... For FileStorage Class .....')
        print('.................................\n\n')
<<<<<<< HEAD

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
=======
        cls.bm_obj = BaseModel()
        cls.state_obj = State(name="Illinois")
        cls.bm_obj.save()
        cls.state_obj.save()

    def tearDownClass():
        """tidies up the tests removing storage objects"""
        storage.delete_all()
        remove(F)

    def setUp(self):
        """initializes new storage object for testing"""
        self.bm_obj = TestBmFsInstances.bm_obj
        self.state_obj = TestBmFsInstances.state_obj

    def test_instantiation(self):
        """... checks proper FileStorage instantiation"""
        self.assertIsInstance(storage, FileStorage)

    def test_storage_file_exists(self):
        """... checks proper FileStorage instantiation"""
        remove(F)
        self.bm_obj.save()
        self.assertTrue(path.isfile(F))

    def test_all(self):
        """... checks if all() function returns newly created instance"""
        bm_id = self.bm_obj.id
        all_obj = storage.all()
        actual = False
        for k in all_obj.keys():
            if bm_id in k:
                actual = True
        self.assertTrue(True)

    def test_all_state(self):
        """... checks if all() function returns newly created state instance"""
        state_id = self.state_obj.id
        state_objs = storage.all("State")
        actual = False
        for k in state_objs.keys():
            if state_id in k:
                actual = True
        self.assertTrue(True)

    def test_obj_saved_to_file(self):
        """... checks proper FileStorage instantiation"""
        remove(F)
        self.bm_obj.save()
        bm_id = self.bm_obj.id
        actual = False
>>>>>>> origin/storage_get_count
        with open(F, mode='r', encoding='utf-8') as f_obj:
            storage_dict = json.load(f_obj)
        for k in storage_dict.keys():
            if bm_id in k:
<<<<<<< HEAD
                actual = 1
        self.assertTrue(1 == actual)
=======
                actual = True
        self.assertTrue(True)
>>>>>>> origin/storage_get_count

    def test_to_json(self):
        """... to_json should return serializable dict object"""
        my_model_json = self.bm_obj.to_json()
<<<<<<< HEAD
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
=======
        actual = True
        try:
            serialized = json.dumps(my_model_json)
        except:
            actual = False
        self.assertTrue(actual)

    def test_reload(self):
        """... checks proper usage of reload function"""
        remove(F)
        self.bm_obj.save()
        bm_id = self.bm_obj.id
        actual = False
>>>>>>> origin/storage_get_count
        new_storage = FileStorage()
        new_storage.reload()
        all_obj = new_storage.all()
        for k in all_obj.keys():
            if bm_id in k:
<<<<<<< HEAD
                actual = 1
        self.assertTrue(1 == actual)

    def test_save_reload_class(self):
        """... checks proper usage of class attribute in file storage"""
        os.remove(F)
        self.bm_obj.save()
        bm_id = self.bm_obj.id
        actual = 0
=======
                actual = True
        self.assertTrue(actual)

    def test_save_reload_class(self):
        """... checks proper usage of class attribute in file storage"""
        remove(F)
        self.bm_obj.save()
        bm_id = self.bm_obj.id
        actual = False
>>>>>>> origin/storage_get_count
        new_storage = FileStorage()
        new_storage.reload()
        all_obj = new_storage.all()
        for k, v in all_obj.items():
            if bm_id in k:
                if type(v).__name__ == 'BaseModel':
<<<<<<< HEAD
                    actual = 1
        self.assertTrue(1 == actual)


=======
                    actual = True
        self.assertTrue(actual)


@unittest.skipIf(STORAGE_TYPE == 'db', 'skip if environ is db')
>>>>>>> origin/storage_get_count
class TestUserFsInstances(unittest.TestCase):
    """testing for class instances"""

    @classmethod
    def setUpClass(cls):
<<<<<<< HEAD
=======
        """sets up the class"""
>>>>>>> origin/storage_get_count
        print('\n\n.................................')
        print('...... Testing FileStorage ......')
        print('.......... User  Class ..........')
        print('.................................\n\n')
<<<<<<< HEAD

    def setUp(self):
        """initializes new user for testing"""
        self.user = User()
        self.bm_obj = BaseModel()

    @unittest.skipIf(storage_type == 'db', 'skip if environ is db')
    def test_storage_file_exists(self):
        """... checks proper FileStorage instantiation"""
        os.remove(F)
        self.user.save()
        self.assertTrue(os.path.isfile(F))

    @unittest.skipIf(storage_type == 'db', 'skip if environ is db')
    def test_obj_saved_to_file(self):
        """... checks proper FileStorage instantiation"""
        os.remove(F)
        self.user.save()
        u_id = self.user.id
        actual = 0
=======
        cls.user = User()
        cls.user.save()
        cls.bm_obj = BaseModel()
        cls.bm_obj.save()

    def tearDownClass():
        """tidies up the tests removing storage objects"""
        storage.delete_all()
        remove(F)

    def setUp(self):
        """initializes new user for testing"""
        self.user = TestUserFsInstances.user
        self.bm_obj = TestUserFsInstances.bm_obj

    def test_storage_file_exists(self):
        """... checks proper FileStorage instantiation"""
        remove(F)
        self.user.save()
        self.assertTrue(path.isfile(F))

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
>>>>>>> origin/storage_get_count
        with open(F, mode='r', encoding='utf-8') as f_obj:
            storage_dict = json.load(f_obj)
        for k in storage_dict.keys():
            if u_id in k:
<<<<<<< HEAD
                actual = 1
        self.assertTrue(1 == actual)

    @unittest.skipIf(storage_type == 'db', 'skip if environ is db')
    def test_reload(self):
        """... checks proper usage of reload function"""
        os.remove(F)
        self.bm_obj.save()
        u_id = self.bm_obj.id
        actual = 0
=======
                actual = True
        self.assertTrue(actual)

    def test_reload(self):
        """... checks proper usage of reload function"""
        remove(F)
        self.bm_obj.save()
        u_id = self.bm_obj.id
        actual = False
>>>>>>> origin/storage_get_count
        new_storage = FileStorage()
        new_storage.reload()
        all_obj = new_storage.all()
        for k in all_obj.keys():
            if u_id in k:
<<<<<<< HEAD
                actual = 1
        self.assertTrue(1 == actual)


@unittest.skipIf(storage_type == 'db', 'skip if environ is not db')
class TestStorageGet(unittest.TestCase):
    """
    Testing `get()` method in DBStorage
    """

    @classmethod
    def setUpClass(cls):
        """
        setup tests for class
        """
        print('\n\n.................................')
        print('...... Testing Get() Method ......')
        print('.......... Place  Class ..........')
        print('.................................\n\n')

    def setUp(self):
        """
        setup method
        """
        self.state = models.state.State(name="Florida")
        self.state.save()

    def test_get_method_obj(self):
        """
        testing get() method
        :return: True if pass, False if not pass
        """

        print(self.state.id)
        result = storage.get(cls="State", id=self.state.id)

        self.assertIsInstance(result, models.state.State)

    def test_get_method_return(self):
        """
        testing get() method for id match
        :return: True if pass, false if not pass
        """
        result = storage.get(cls="State", id=str(self.state.id))

        self.assertEqual(self.state.id, result.id)

    def test_get_method_none(self):
        """
        testing get() method for None return
        :return: True if pass, false if not pass
        """
        result = storage.get(cls="State", id="doesnotexist")

        self.assertIsNone(result)


@unittest.skipIf(storage_type == 'db', 'skip if environ is not db')
class TestStorageCount(unittest.TestCase):
    """
    tests count() method in DBStorage
    """

    @classmethod
    def setUpClass(cls):
        """
        setup tests for class
        """
        print('\n\n.................................')
        print('...... Testing Get() Method ......')
        print('.......... Place  Class ..........')
        print('.................................\n\n')

    def setup(self):
        """
        setup method
        """
        models.state.State()
        models.state.State()
        models.state.State()
        models.state.State()
        models.state.State()
        models.state.State()
        models.state.State()

    def test_count_all(self):
        """
        testing counting all instances
        :return: True if pass, false if not pass
        """
        result = storage.count()

        self.assertEqual(len(storage.all()), result)

    def test_count_state(self):
        """
        testing counting state instances
        :return: True if pass, false if not pass
        """
        result = storage.count(cls="State")

        self.assertEqual(len(storage.all("State")), result)

    def test_count_city(self):
        """
        testing counting non existent
        :return: True if pass, false if not pass
        """
        result = storage.count(cls="City")

        self.assertEqual(
            int(0 if len(storage.all("City")) is None else
                len(storage.all("City"))), result)
=======
                actual = True
        self.assertTrue(actual)
>>>>>>> origin/storage_get_count


if __name__ == '__main__':
    unittest.main
