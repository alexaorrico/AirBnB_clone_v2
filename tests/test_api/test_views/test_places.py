#!/usr/bin/python3
'''places unittest'''
import unittest
import json
from models.city import City
from models.place import Place
from models.user import User
from models.amenity import Amenity
from models.state import State
from models import storage
from api.v1.app import app
from flask import Response



class TestPlaceAppViews(unittest.TestCase):
    def setUp(self):
        # Create a test client
        self.app = app.test_client()
        # Create a new city and user for testing
        self.test_city = City(name="Test City")
        self.test_city.save()
        self.test_user = User(email="test@example.com", password="testpassword")
        self.test_user.save()

    def tearDown(self):
        # Clean up the test city and user after each test
        self.test_city.delete()
        self.test_user.delete()

    def test_get_place(self):
        new_place = Place(name="Test Place", city_id=self.test_city.id, user_id=self.test_user.id)
        new_place.save()

        response = self.app.get('/api/v1/places/{}'.format(new_place.id))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['id'], new_place.id)

        new_place.delete()

    def test_get_place_not_found(self):
        response = self.app.get('/api/v1/places/12345')  # Non-existing ID
        self.assertEqual(response.status_code, 404)

    def test_delete_place(self):
        new_place = Place(name="Test Place", city_id=self.test_city.id, user_id=self.test_user.id)
        new_place.save()

        response = self.app.delete('/api/v1/places/{}'.format(new_place.id))
        self.assertEqual(response.status_code, 200)
        # Verify that the place has been deleted
        deleted_place = storage.get(Place, new_place.id)
        self.assertIsNone(deleted_place)

    def test_delete_place_not_found(self):
        response = self.app.delete('/api/v1/places/12345')  # Non-existing ID
        self.assertEqual(response.status_code, 404)

    def test_create_place(self):
        new_place_data = {"name": "New Place", "user_id": self.test_user.id}
        response = self.app.post('/api/v1/cities/{}/places'.format(self.test_city.id), json=new_place_data)
        data = json.loads(response.get_data(as_text=True))
        self.assertIn('id', data)
        self.assertEqual(data['name'], new_place_data['name'])

    def test_update_place(self):
        new_place = Place(name="Test Place", city_id=self.test_city.id, user_id=self.test_user.id)
        new_place.save()

        updated_place_data = {"name": "Updated Place"}
        response = self.app.put('/api/v1/places/{}'.format(new_place.id), json=updated_place_data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['name'], updated_place_data['name'])

        new_place.delete()

    def test_update_place_not_found(self):
        response = self.app.put('/api/v1/places/12345', json={"name": "Updated Place"})
        self.assertEqual(response.status_code, 404)

    def test_places_search(self):
        response = self.app.post('/api/v1/places_search', json={"states": [self.test_city.state_id]})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertTrue(isinstance(data, list))

if __name__ == '__main__':
    unittest.main()
