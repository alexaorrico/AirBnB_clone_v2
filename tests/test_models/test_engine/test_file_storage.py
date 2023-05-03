from datetime import datetime
from models import *
from models.engine.file_storage import FileStorage
import os
import unittest


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE', 'fs') == 'db',
                 "db does not have FileStorage")
class Test_FileStorage(unittest.TestCase):
    """
    Test the file storage class
    """

    def setUp(self):
        self.store = FileStorage()

        test_args = {'updated_at': datetime(2017, 2, 12, 00, 31, 53, 331997),
                     'id': 'f519fb40-1f5c-458b-945c-2ee8eaaf4900',
                     'created_at': datetime(2017, 2, 12, 00, 31, 53, 331900)}
        self.model = BaseModel(**test_args)

        self.test_len = len(self.store.all())

#    @classmethod
#    def tearDownClass(cls):
#        import os
#        if os.path.isfile("test_file.json"):
#            os.remove('test_file.json')

    def test_all(self):
        self.assertEqual(len(self.store.all()), self.test_len)

    def test_all_arg(self):
        """test all(State)"""
        new_obj = State()
        new_obj.save()
        everything = self.store.all()
        nb_states = 0
        for e in everything.values():
            if e.__class__.__name__ == "State":
                nb_states += 1
        self.assertEqual(len(self.store.all("State")), nb_states)

# should test with a bad class name

    def test_new(self):
        # note: we cannot assume order of test is order written
        test_len = len(self.store.all())
        # self.assertEqual(len(self.store.all()), self.test_len)
        new_obj = State()
        new_obj.save()
        self.assertEqual(len(self.store.all()), test_len + 1)
        a = BaseModel()
        a.save()
        self.assertEqual(len(self.store.all()), self.test_len + 2)

    def test_save(self):
        self.test_len = len(self.store.all())
        a = BaseModel()
        a.save()
        self.assertEqual(len(self.store.all()), self.test_len + 1)
        b = User()
        self.assertNotEqual(len(self.store.all()), self.test_len + 2)
        b.save()
        self.assertEqual(len(self.store.all()), self.test_len + 2)

    def test_reload(self):
        self.model.save()
        a = BaseModel()
        a.save()
        self.store.reload()
        for value in self.store.all().values():
            self.assertIsInstance(value.created_at, datetime)

    def test_state(self):
        """test State creation with an argument"""
        a = State(name="Kamchatka", id="Kamchatka666")
        a.save()
        self.assertIn("Kamchatka666", self.store.all("State").keys())

    def test_count(self):
        """test count all"""
        test_len = len(self.store.all())
        a = Amenity(name="test_amenity")
        a.save()
        self.assertEqual(test_len + 1, self.store.count())

    def test_count_arg(self):
        """test count with an argument"""
        test_len = len(self.store.all("Amenity"))
        a = Amenity(name="test_amenity_2")
        a.save()
        self.assertEqual(test_len + 1, self.store.count("Amenity"))

    def test_count_bad_arg(self):
        """test count with dummy class name"""
        self.assertEqual(-1, self.store.count("Dummy"))

    def test_get(self):
        """test get with valid cls and id"""
        a = Amenity(name="test_amenity3", id="test_3")
        a.save()
        result = self.store.get("Amenity", "test_3")
        self.assertEqual(a.name, result.name)
        self.assertEqual(a.created_at, result.created_at)

    def test_get_bad_cls(self):
        """test get with invalid cls"""
        result = self.store.get("Dummy", "test")
        self.assertIsNone(result)

    def test_get_bad_id(self):
        """test get with invalid id"""
        result = self.store.get("State", "very_bad_id")
        self.assertIsNone(result)


if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(1, os.path.join(os.path.split(__file__)[0], '../../..'))
    from models import *
    from models.engine.file_storage import FileStorage
    unittest.main()
