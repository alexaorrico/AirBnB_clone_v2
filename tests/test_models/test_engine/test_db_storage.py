from datetime import datetime
from models import *
from models.amenity import Amenity
from models.base_model import Base
from models.engine.db_storage import DBStorage
from models.state import State
import os.path
from os import getenv
import unittest


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE', 'fs') != 'db', "db")
class Test_DBStorage(unittest.TestCase):
    """
    Test the file storage class
    """
    @classmethod
    def setUpClass(cls):
        """We cannot create a new session as everything depends on storage in
        init"""
        test_args = {'updated_at': datetime(2017, 2, 12, 00, 31, 53, 331997),
                     'id': "0234",
                     'created_at': datetime(2017, 2, 12, 00, 31, 53, 331900),
                     'name': 'wifi'}
        cls.model = Amenity(**test_args)

    @classmethod
    def tearDownClass(cls):
        storage.close()

    def test_all(self):
        l1 = len(storage.all('State'))
        state = State(name="State test all")
        state.save()
        output = storage.all('State')
        self.assertEqual(len(output), l1 + 1)
        self.assertIn(state.id, output.keys())

    def test_new(self):
        # note: we cannot assume order of test is order written
        test_len = len(storage.all())
        # self.assertEqual(len(storage.all()), self.test_len)
        self.model.save()
        self.assertEqual(len(storage.all()), test_len + 1)
        a = Amenity(name="thing")
        a.save()
        self.assertEqual(len(storage.all()), test_len + 2)

    def test_save(self):
        test_len = len(storage.all())
        a = Amenity(name="another")
        a.save()
        self.assertEqual(len(storage.all()), test_len + 1)
        b = State(name="california")
        self.assertNotEqual(len(storage.all()), test_len + 2)
        b.save()
        self.assertEqual(len(storage.all()), test_len + 2)

    def test_delete(self):
        all_storage = storage.all()
        test_len = len(all_storage)
        for v in all_storage.values():
            storage.delete(v)
            test_len -= 1
            self.assertGreaterEqual(test_len, storage.count())

    def test_reload(self):
        """not actually testing reload as it creates a parallel new session"""
        a = Amenity(name="different")
        a.save()
        for value in storage.all().values():
            self.assertIsInstance(value.created_at, datetime)

    def test_state(self):
        """test State creation with a keyword argument"""
        a = State(name="Kamchatka", id="Kamchatka666")
        a.save()
        self.assertIn("Kamchatka666", storage.all("State").keys())

    def test_count(self):
        """test count all"""
        test_len = len(storage.all())
        a = Amenity(name="test_amenity")
        a.save()
        self.assertEqual(test_len + 1, storage.count())
        b = State(name="State test count")
        b.save()
        self.assertEqual(test_len + 2, storage.count())
        storage.delete(b)
        self.assertEqual(test_len + 1, storage.count())

    def test_count_amenity(self):
        """test count with an argument"""
        test_len = len(storage.all("Amenity"))
        a = Amenity(name="test_amenity_2")
        a.save()
        self.assertEqual(test_len + 1, storage.count("Amenity"))
        storage.delete(a)
        self.assertEqual(test_len, storage.count("Amenity"))

    def test_count_state(self):
        """test count with an argument"""
        test_len = len(storage.all("State"))
        a = State(name="test_state_count_arg")
        a.save()
        self.assertEqual(test_len + 1, storage.count("State"))
        storage.delete(a)
        self.assertEqual(test_len, storage.count("State"))

    def test_count_bad_arg(self):
        """test count with dummy class name"""
        self.assertEqual(-1, storage.count("Dummy"))

    def test_get_amenity(self):
        """test get with valid cls and id"""
        a = Amenity(name="test_amenity3", id="test_3")
        a.save()
        result = storage.get("Amenity", "test_3")
        self.assertEqual(a.name, result.name)
        # does not work as the database loses last argument tzinfo for datetime
        # self.assertEqual(a.created_at, result.created_at)
        self.assertEqual(a.created_at.year, result.created_at.year)
        self.assertEqual(a.created_at.month, result.created_at.month)
        self.assertEqual(a.created_at.day, result.created_at.day)
        self.assertEqual(a.created_at.hour, result.created_at.hour)
        self.assertEqual(a.created_at.minute, result.created_at.minute)
        self.assertEqual(a.created_at.second, result.created_at.second)
        storage.delete(a)
        result = storage.get("Amenity", "test_3")
        self.assertIsNone(result)

    def test_get_state(self):
        """test get with valid cls and id"""
        a = State(name="test_state3", id="test_3")
        a.save()
        result = storage.get("State", "test_3")
        self.assertEqual(a.name, result.name)
        # does not work as the database loses last argument tzinfo for datetime
        # self.assertEqual(a.created_at, result.created_at)
        self.assertEqual(a.created_at.year, result.created_at.year)
        self.assertEqual(a.created_at.month, result.created_at.month)
        self.assertEqual(a.created_at.day, result.created_at.day)
        self.assertEqual(a.created_at.hour, result.created_at.hour)
        self.assertEqual(a.created_at.minute, result.created_at.minute)
        self.assertEqual(a.created_at.second, result.created_at.second)
        storage.delete(a)
        result = storage.get("State", "test_3")
        self.assertIsNone(result)

    def test_get_bad_cls(self):
        """test get with invalid cls"""
        result = storage.get("Dummy", "test")
        self.assertIsNone(result)

    def test_get_bad_id(self):
        """test get with invalid id"""
        result = storage.get("State", "very_bad_id")
        self.assertIsNone(result)


if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(1, os.path.join(os.path.split(__file__)[0], '../../..'))
    from models import *
    from models.engine.file_storage import FileStorage
    unittest.main()
