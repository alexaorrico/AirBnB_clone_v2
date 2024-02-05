import unittest
import json
from models.user import User
from models import storage
from api.v1.app import app
from flask import Response


class TestUserAppViews(unittest.TestCase):
    def setUp(self):
        # Create a test client
        self.app = app.test_client()
        # Create a new user for testing
        self.test_user = User(
            email="test@example.com",
            password="testpassword")
        self.test_user.save()

    def tearDown(self):
        # Clean up the test user after each test
        self.test_user.delete()

    def test_all_user(self):
        response = self.app.get('/api/v1/users')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertTrue(isinstance(data, list))

    def test_user_by_id(self):
        response = self.app.get('/api/v1/users/{}'.format(self.test_user.id))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['id'], self.test_user.id)

    def test_user_by_id_not_found(self):
        response = self.app.get('/api/v1/users/12345')  # Non-existing ID
        self.assertEqual(response.status_code, 404)

    def test_delete_by_id(self):
        response = self.app.delete(
            '/api/v1/users/{}'.format(self.test_user.id))
        self.assertEqual(response.status_code, 200)
        deleted_user = storage.get(User, self.test_user.id)
        self.assertIsNone(deleted_user)

    def test_delete_by_id_not_found(self):
        response = self.app.delete('/api/v1/users/12345')  # Non-existing ID
        self.assertEqual(response.status_code, 404)

    def test_create_user(self):
        new_user_data = {
            "email": "newuser@example.com",
            "password": "newpassword"}
        response = self.app.post('/api/v1/users', json=new_user_data)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.get_data(as_text=True))
        self.assertIn('id', data)
        self.assertEqual(data['email'], new_user_data['email'])

    def test_create_user_missing_email(self):
        invalid_user_data = {"password": "newpassword"}
        response = self.app.post('/api/v1/users', json=invalid_user_data)
        self.assertEqual(response.status_code, 400)

    def test_create_user_missing_password(self):
        invalid_user_data = {"email": "newuser@example.com"}
        response = self.app.post('/api/v1/users', json=invalid_user_data)
        self.assertEqual(response.status_code, 400)

    def test_update_user(self):
        updated_user_data = {
            "email": "updated@example.com",
            "password": "updatedpassword"}
        response = self.app.put('/api/v1/users/{}'.format(
                                self.test_user.id), json=updated_user_data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['email'], updated_user_data['email'])

    def test_update_user_not_found(self):
        response = self.app.put(
            '/api/v1/users/12345',
            json={
                "email": "updated@example.com",
                "password": "updatedpassword"})
        self.assertEqual(response.status_code, 404)

    def test_update_user_invalid_json(self):
        response = self.app.put(
            '/api/v1/users/{}'.format(
                self.test_user.id),
            data="Invalid JSON",
            content_type="application/json")
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
