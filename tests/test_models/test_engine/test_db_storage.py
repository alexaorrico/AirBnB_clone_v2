#!/usr/bin/python3
''' Unit tests for DB storage '''
import os
import unittest
import models
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.state import State


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                 "Only want to test Database storage")
class testDBStorage(unittest.TestCase):
    '''
    Testing the DB storage class
    '''
    def test_existence_user(self):
        '''
        Testing if User class is being created properly
        '''
        user = User(email="john@snow.com", password="johnpwd")
        user.save()
        if user.id in models.storage.all('User'):
            self.assertTrue(user.password, "johnpwd")

    def test_existence_amenity(self):
        '''
        Testing if Amenity class is being created properly
        '''
        amenity = Amenity(name="Wifi")
        amenity.save()
        if amenity.id in models.storage.all():
            self.assertTrue(amenity.name, "Wifi")

    def test_existence_state(self):
        '''
        Testing if State class is being created properly
        '''
        state = State(name="Alaska")
        state.save()
        if state.id in models.storage.all():
            self.assertTrue(state.name, "Alaska")

    def test_all_method(self):
        '''
        Testing if all() method returns all instances
        '''
        state = State(name="Cali")
        state.save()
        amenity = Amenity(name="Cable")
        amenity.save()
        user = User(email="john@snow.com", password="johnpwd")
        user.save()
        test_me = str(state.id) + str(amenity.id) + str(user.id)
        if test_me in models.storage.all():
            self.assertTrue(state.name, "Cali")

    def test_delete_method(self):
        '''
            Tests the delete method in db_storage
        '''
        state = State(name="Texas")
        state.save()
        all_stored = models.storage.all()
        models.storage.delete(state)
        self.assertTrue(all_stored["State." + state.id])

    def test_get_count_all(self):
        '''
            Tests the count method in db_storage
        '''
        all_obj = models.storage.all()
        count_all_obj = models.storage.count()
        self.assertEqual(len(all_obj), count_all_obj)

    def test_get_count_cls(self):
        '''
            Tests the count method in db_storage with class name given
        '''
        all_obj = models.storage.all('State')
        count_all_obj = models.storage.count('State')
        self.assertEqual(len(all_obj), count_all_obj)

    def test_get_method(self):
        '''
            Tests the get method
        '''
        state = State(name="Texas")
        state.save()
        state_id = state.id
        get_state = models.storage.get('State', state_id)
        self.assertEqual(state, get_state)

    def test_get_method_cls(self):
        '''
            Tests the get method without instance id
        '''
        get_state = models.storage.get('State', 'jlk124343')
        self.assertEqual(get_state, None)
