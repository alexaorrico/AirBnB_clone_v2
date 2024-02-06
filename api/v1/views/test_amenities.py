import unittest
from flask import json
from api.v1.views.amenities import app_views
from models import storage
from models.amenity import Amenity


class TestAmenities(unittest.TestCase):
    def setUp(self):
        self.app = app_views.test_client()

    def test_get_amenities(self):
        response = self.app.get('/api/v1/amenities')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsInstance(data, list)

    def test_create_amenity(self):
        data = {
            'name': 'Swimming Pool'
        }
        response = self.app.post('/api/v1/amenities',
                                data=json.dumps(data),
                                content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsInstance(data, dict)
        self.assertIn('id', data)

    def test_create_amenity_missing_name(self):
        data = {}
        response = self.app.post('/api/v1/amenities',
                                data=json.dumps(data),
                                content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_update_amenity(self):
        amenity = Amenity(name='Gym')
        amenity.save()
        data = {
            'name': 'Fitness Center'
        }
        response = self.app.put(f'/api/v1/amenities/{amenity.id}',
                                data=json.dumps(data),
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsInstance(data, dict)
        self.assertEqual(data['name'], 'Fitness Center')

    def test_update_amenity_not_found(self):
        data = {
            'name': 'Fitness Center'
        }
        response = self.app.put('/api/v1/amenities/nonexistent_id',
                                data=json.dumps(data),
                                content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_delete_amenity(self):
        amenity = Amenity(name='Sauna')
        amenity.save()
        response = self.app.delete(f'/api/v1/amenities/{amenity.id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data, {})

    def test_delete_amenity_not_found(self):
        response = self.app.delete('/api/v1/amenities/nonexistent_id')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()