import unittest
import json
from models import storage
from models.state import State
from models.city import City
from api.v1.app import app

class TestCityViews(unittest.TestCase):
    def setUp(self):
        """Set up for the tests"""
        self.app = app.test_client()
        self.app.testing = True

        # Create a test state
        self.state = State(name="TestState")
        self.state.save()

        # Create a test city
        self.city = City(name="TestCity", state_id=self.state.id)
        self.city.save()

    def tearDown(self):
        """Tear down after the tests"""
        self.city.delete()
        self.state.delete()
        storage.save()

    def test_get_cities(self):
        """Test retrieving cities of a state"""
        response = self.app.get(f'/api/v1/states/{self.state.id}/cities')
        self.assertEqual(response.status_code, 200)
        self.assertIn('TestCity', str(response.data))

    def test_get_city(self):
        """Test retrieving a city"""
        response = self.app.get(f'/api/v1/cities/{self.city.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('TestCity', str(response.data))

    def test_get_city_not_found(self):
        """Test retrieving a city that does not exist"""
        response = self.app.get('/api/v1/cities/not_an_id')
        self.assertEqual(response.status_code, 404)

    def test_delete_city(self):
        """Test deleting a city"""
        response = self.app.delete(f'/api/v1/cities/{self.city.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'{}')
        # Verify the city is deleted
        response = self.app.get(f'/api/v1/cities/{self.city.id}')
        self.assertEqual(response.status_code, 404)

    def test_create_city(self):
        """Test creating a city"""
        new_city_data = json.dumps({"name": "NewCity"})
        response = self.app.post(f'/api/v1/states/{self.state.id}/cities',
                                 data=new_city_data,
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('NewCity', str(response.data))

    def test_create_city_not_found(self):
        """Test creating a city in a non-existent state"""
        new_city_data = json.dumps({"name": "NewCity"})
        response = self.app.post('/api/v1/states/not_an_id/cities',
                                 data=new_city_data,
                                 content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_create_city_not_json(self):
        """Test creating a city with invalid JSON"""
        response = self.app.post(f'/api/v1/states/{self.state.id}/cities',
                                 data="Not a JSON",
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Not a JSON', str(response.data))

    def test_create_city_missing_name(self):
        """Test creating a city without a name"""
        new_city_data = json.dumps({})
        response = self.app.post(f'/api/v1/states/{self.state.id}/cities',
                                 data=new_city_data,
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing name', str(response.data))

    def test_update_city(self):
        """Test updating a city"""
        update_data = json.dumps({"name": "UpdatedCity"})
        response = self.app.put(f'/api/v1/cities/{self.city.id}',
                                data=update_data,
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('UpdatedCity', str(response.data))

    def test_update_city_not_found(self):
        """Test updating a non-existent city"""
        update_data = json.dumps({"name": "UpdatedCity"})
        response = self.app.put('/api/v1/cities/not_an_id',
                                data=update_data,
                                content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_update_city_not_json(self):
        """Test updating a city with invalid JSON"""
        response = self.app.put(f'/api/v1/cities/{self.city.id}',
                                data="Not a JSON",
                                content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Not a JSON', str(response.data))

if __name__ == '__main__':
    unittest.main()
