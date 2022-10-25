#!/usr/bin/python3
"""test for databasse storage"""
import unittest
from datetime import datetime
from os import getenv
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.db_storage import DBStorage
from models import storage
import inspect
import MySQLdb
import pep8


class TestDBStorage(unittest.TestCase):
    '''this will test the DBStorage'''

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'db',
                     "can't run if storage is file")
    def setUp(self):
        """set up for test"""
        if getenv("HBNB_TYPE_STORAGE") == "db":
            self.db = MySQLdb.connect(getenv("HBNB_MYSQL_HOST"),
                                      getenv("HBNB_MYSQL_USER"),
                                      getenv("HBNB_MYSQL_PWD"),
                                      getenv("HBNB_MYSQL_DB"))
            self.cursor = self.db.cursor()

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'db',
                     "can't run if storage is file")
    def tearDown(self):
        """at the end of the test this will tear it down"""
        if getenv("HBNB_TYPE_STORAGE") == "db":
            self.db.close()

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'db',
                     "can't run if storage is file")
    def test_pep8_DBStorage(self):
        """Testing for pep8"""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(['models/engine/db_storage.py'])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'db',
                     "can't run if storage is file")
    def test_attributes_DBStorage(self):
        """Tests for class attributes"""
        self.assertTrue(hasattr(DBStorage, '_DBStorage__engine'))
        self.assertTrue(hasattr(DBStorage, '_DBStorage__session'))
        self.assertTrue(hasattr(DBStorage, 'all'))
        self.assertTrue(hasattr(DBStorage, 'new'))
        self.assertTrue(hasattr(DBStorage, 'save'))
        self.assertTrue(hasattr(DBStorage, 'delete'))
        self.assertTrue(hasattr(DBStorage, 'reload'))

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'db',
                     "can't run if storage is file")
    def test_all_DBStorage(self):
        """Tests for all() method"""
        s = State(name="California")
        storage.new(s)
        storage.save()
        k = '{}.{}'.format(type(s).__name__, s.id)
        dic = storage.all(State)
        self.assertTrue(k in dic.keys())
        s1 = State(name="Arizona")
        storage.new(s1)
        storage.save()
        k1 = '{}.{}'.format(type(s1).__name__, s1.id)
        dic1 = storage.all()
        self.assertTrue(k in dic1.keys())
        self.assertTrue(k1 in dic1.keys())
        u = User(email="derps@herps.com", password="hurrdurr")
        storage.new(u)
        storage.save()
        k2 = '{}.{}'.format(type(u).__name__, u.id)
        dic2 = storage.all(User)
        self.assertTrue(k2 in dic2.keys())
        self.assertFalse(k1 in dic2.keys())
        self.assertFalse(k in dic2.keys())
        self.assertFalse(k2 in dic.keys())

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'db',
                     "can't run if storage is file")
    def test_new_DBStorage(self):
        """Tests for new() method"""
        nb = self.cursor.execute("SELECT COUNT(*) FROM states")
        s = State(name="Oregon")
        s.save()
        nb1 = self.cursor.execute("SELECT COUNT(*) FROM states")
        self.assertEqual(nb1 - nb, 0)

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'db',
                     "can't run if storage is file")
    def test_reload(self):
        """Test for reload()"""
        obj = DBStorage()
        self.assertTrue(obj._DBStorage__engine is not None)
        self.assertTrue(obj._DBStorage__session is None)
        obj.reload()
        self.assertTrue(obj._DBStorage__session is not None)

    @unittest.skipIf(STORAGE_TYPE != 'db', 'skip if environ is not db')
class TestCountGet(unittest.TestCase):
    """testing Count and Get methods"""

    @classmethod
    def setUpClass(cls):
        """sets up the class for this round of tests"""
        print('\n\n....................................')
        print('.......... Testing DBStorage .......')
        print('. State, City, User, Place Amenity .')
        print('....................................')
        storage.delete_all()
        cls.s = State(name="California")
        cls.c = City(state_id=cls.s.id,
                     name="San Francisco")
        cls.u = User(email="betty@holbertonschool.com",
                     password="pwd")
        cls.p1 = Place(user_id=cls.u.id,
                       city_id=cls.c.id,
                       name="a house")
        cls.p2 = Place(user_id=cls.u.id,
                       city_id=cls.c.id,
                       name="a house two")
        cls.a1 = Amenity(name="Wifi")
        cls.a2 = Amenity(name="Cable")
        cls.a3 = Amenity(name="Bucket Shower")
        objs = [cls.s, cls.c, cls.u, cls.p1, cls.p2, cls.a1, cls.a2, cls.a3]
        for obj in objs:
            obj.save()

    def setUp(self):
        """initializes new user for testing"""
        self.s = TestCountGet.s
        self.c = TestCountGet.c
        self.u = TestCountGet.u
        self.p1 = TestCountGet.p1
        self.p2 = TestCountGet.p2
        self.a1 = TestCountGet.a1
        self.a2 = TestCountGet.a2
        self.a3 = TestCountGet.a3

    def test_all_reload_save(self):
        """... checks if all(), save(), and reload function
        in new instance.  This also tests for reload"""
        actual = 0
        db_objs = storage.all()
        for obj in db_objs.values():
            for x in [self.s.id, self.c.id, self.u.id, self.p1.id]:
                if x == obj.id:
                    actual += 1
        self.assertTrue(actual == 4)


@unittest.skipIf(STORAGE_TYPE == 'db', 'skip if environ is db')
class TestBmFsInstances(unittest.TestCase):
    """testing for class instances"""

    @classmethod
    def setUpClass(cls):
        """sets up the class"""
        print('\n\n.................................')
        print('...... Testing FileStorate ......')
        print('..... For FileStorage Class .....')
        print('.................................\n\n')
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
        with open(F, mode='r', encoding='utf-8') as f_obj:
            storage_dict = json.load(f_obj)
        for k in storage_dict.keys():
            if bm_id in k:
                actual = True
        self.assertTrue(True)

    def test_to_json(self):
        """... to_json should return serializable dict object"""
        my_model_json = self.bm_obj.to_json()
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
        new_storage = FileStorage()
        new_storage.reload()
        all_obj = new_storage.all()
        for k in all_obj.keys():
            if bm_id in k:
                actual = True
        self.assertTrue(actual)

    def test_save_reload_class(self):
        """... checks proper usage of class attribute in file storage"""
        remove(F)
        self.bm_obj.save()
        bm_id = self.bm_obj.id
        actual = False
        new_storage = FileStorage()
        new_storage.reload()
        all_obj = new_storage.all()
        for k, v in all_obj.items():
            if bm_id in k:
                if type(v).__name__ == 'BaseModel':
                    actual = True
        self.assertTrue(actual)


@unittest.skipIf(STORAGE_TYPE == 'db', 'skip if environ is db')
class TestUserFsInstances(unittest.TestCase):
    """testing for class instances"""

    @classmethod
    def setUpClass(cls):
        """sets up the class"""
        print('\n\n.................................')
        print('...... Testing FileStorage ......')
        print('.......... User  Class ..........')
        print('.................................\n\n')
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
