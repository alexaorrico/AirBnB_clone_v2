#!/usr/bin/python3
''' testing database storage '''
import unittest
import pep8
import json
import os
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage
from models import storage


class TestDBStorage(unittest.TestCase):
    ''' testing the DBStorage '''

    def test_pep8_FileStorage(self):
        ''' Testing pep8 style '''
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(['models/engine/db_storage.py'])
        self.assertEqual(p.total_errors, 0, "fix pep8")

        def setUp(self):
            self.db_storage = storage.DBStorage()
        self.db_storage.reload()

    def tearDown(self):
        self.db_storage.close()

    def test_get_existing_object(self):
        """Test retrieving an existing object using get()"""
        new_state = (
            self.
            _extracted_from__extracted_from_test_count_objects_by_class_5_3()
        )
        retrieved_state = self.db_storage.get(State, new_state.id)
        self.assertEqual(retrieved_state, new_state)

    def test_get_nonexistent_object(self):
        """Test retrieving a nonexistent object using get()"""
        retrieved_state = self.db_storage.get(State, "nonexistent-id")
        self.assertIsNone(retrieved_state)

    def test_count_all_objects(self):
        """Test counting all objects in storage"""
        initial_count = self.db_storage.count()

        self._extracted_from_test_count_objects_by_class_5()
        updated_count = self.db_storage.count()

        self.assertEqual(updated_count, initial_count + 2)

    def test_count_objects_by_class(self):
        """Test counting objects in storage by class"""
        initial_state_count = self.db_storage.count(State)
        initial_city_count = self.db_storage.count(City)

        self._extracted_from_test_count_objects_by_class_5()
        updated_state_count = self.db_storage.count(State)
        updated_city_count = self.db_storage.count(City)

        self.assertEqual(updated_state_count, initial_state_count + 1)
        self.assertEqual(updated_city_count, initial_city_count + 1)

    # TODO Rename this here and in `test_count_all_objects` and\
        # `test_count_objects_by_class`
    def _extracted_from_test_count_objects_by_class_5(self):
        new_state = (
            self.
            _extracted_from__extracted_from_test_count_objects_by_class_5_3()
        )
        new_city = City(name="Los Angeles", state_id=new_state.id)
        storage.new(new_city)
        storage.save()

    # TODO Rename this here and in `test_get_existing_object` and\
        # `_extracted_from_test_count_objects_by_class_5`
    def _extracted_from__extracted_from_test_count_objects_by_class_5_3(self):
        result = State(name="California")
        storage.new(result)
        storage.save()
        return result

    def test_get_positive(self):
        obj = User(name="John")
        self.session.add(obj)
        self.session.commit()
        result = self.get(User, obj.id)
        assert result == obj

    def test_get_negative(self):
        result = self.get(User, 0)
        assert result is None

    def test_count_with_class(self):
        self._extracted_from_test_count_without_class_2()
        result = self.count(User)
        assert result == 2

    def test_count_without_class(self):
        self._extracted_from_test_count_without_class_2()
        result = self.count()
        assert result == 2

    # TODO Rename this here and in `test_count_with_class` and\
    # `test_count_without_class`
    def _extracted_from_test_count_without_class_2(self):
        obj1 = User(name="John")
        obj2 = User(name="Jane")
        self.session.add_all([obj1, obj2])
        self.session.commit()


if __name__ == "__main__":
    unittest.main()
