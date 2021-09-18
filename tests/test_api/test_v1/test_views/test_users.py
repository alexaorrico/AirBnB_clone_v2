#!/usr/bin/python3
import json
from models import storage
from models.state import State
from models.user import User
import os
import requests
import unittest


host = os.environ['HBNB_API_HOST']
port = os.environ['HBNB_API_PORT']
version = '/v1'
api_url = 'http://{}:{}/api{}'.format(host, port, version)


WRONG_STATUS_CODE_MSG = 'Wrong status code!'
WRONG_TYPE_RETURN_MSG = 'Wrong return type return!'
WRONG_OBJ_TYPE_MSG = 'Wrong object type!'
MISSING_LASTNAME_ATTR_MSG = 'Missing last_name!'
MISSING_FIRSTNAME_ATTR_MSG = 'Missing first_name!'
MISSING_EMAIL_ATTR_MSG = 'Missing email!'
MISSING_PASSWORD_ATTR_MSG = 'Missing password!'
MISSING_CREATED_AT_ATTR_MSG = 'Missing created_at!'
MISSING_UPDATED_AT_ATTR_MSG = 'Missing updated_at!'
MISSING_CLASS_ATTR_MSG = 'Missing class!'


class ListUsersApiTest(unittest.TestCase):
    """
        Tests of API list action for User.
    """

    def setUp(self) -> None:
        """
            Set up API list action tests.
        """
        self.url = '{}/users'.format(api_url)

    def testList(self):
        """
            Test valid list action.
        """
        response = requests.get(url=self.url)
        headers = response.headers

        self.assertEqual(response.status_code, 200, WRONG_STATUS_CODE_MSG)
        self.assertEqual(
            headers['Content-Type'], 'application/json', WRONG_TYPE_RETURN_MSG)

    def testCount(self):
        """
            Test list length.
        """
        state = State(name='toto')
        user = User(last_name='toto', first_name='titi',
                    email='email', password='password')
        storage.new(state)
        storage.new(user)
        storage.save()
        initial_count = len(storage.all(User))
        response = requests.get(url=self.url)
        json_data = response.json()

        self.assertEqual(initial_count, len(json_data))

        storage.delete(state)
        storage.delete(user)
        storage.save()

    def testOnlyUser(self):
        """
            Test valid list action with Place content only.
        """
        state = State(name='toto')
        user = User(last_name='toto', first_name='titi',
                    email='email', password='password')
        storage.new(state)
        storage.new(user)
        storage.save()
        response = requests.get(url=self.url)
        json_data = response.json()

        for element in json_data:
            self.assertEqual(element['__class__'], 'User', WRONG_OBJ_TYPE_MSG)
        storage.delete(state)
        storage.delete(user)
        storage.save()


class ShowUsersApiTest(unittest.TestCase):
    """
        Tests of API show action for User.
    """

    def setUp(self) -> None:
        """
            Set up API show action tests.
        """
        self.user = User(last_name='toto', first_name='titi',
                         email='email', password='password')
        self.user_id = self.user.id
        storage.new(self.user)
        storage.save()
        self.url = '{}/users/{}'.format(api_url, self.user.id)
        self.invalid_url = '{}/users/{}'.format(api_url, 'toto')

    def tearDown(self) -> None:
        """
            Tear down table State of database used for tests.
        """
        storage.delete(self.user)
        storage.save()

    def testShow(self):
        """
            Test valid show action.
        """
        response = requests.get(url=self.url)
        headers = response.headers
        json_data = response.json()

        self.assertEqual(response.status_code, 200, WRONG_STATUS_CODE_MSG)
        self.assertEqual(
            headers['Content-Type'], 'application/json', WRONG_TYPE_RETURN_MSG)
        self.assertIn('last_name', json_data, MISSING_LASTNAME_ATTR_MSG)
        self.assertIn('first_name', json_data, MISSING_FIRSTNAME_ATTR_MSG)
        self.assertIn('email', json_data, MISSING_EMAIL_ATTR_MSG)
        self.assertIn('password', json_data, MISSING_PASSWORD_ATTR_MSG)
        self.assertIn('created_at', json_data, MISSING_CREATED_AT_ATTR_MSG)
        self.assertIn('updated_at', json_data, MISSING_UPDATED_AT_ATTR_MSG)
        self.assertIn('__class__', json_data, MISSING_CLASS_ATTR_MSG)
        self.assertEqual(json_data['last_name'], self.user.last_name)
        self.assertEqual(json_data['first_name'], self.user.first_name)
        self.assertEqual(json_data['email'], self.user.email)
        self.assertEqual(json_data['password'], self.user.password)

    def testNotFound(self):
        """
            Test show action when given wrong user_id or no ID at all.
        """
        response = requests.get(url=self.invalid_url)
        headers = response.headers
        json_data = response.json()

        self.assertEqual(response.status_code, 404, WRONG_STATUS_CODE_MSG)
        self.assertEqual(
            headers['Content-Type'], 'application/json', WRONG_TYPE_RETURN_MSG)
        self.assertTrue(self.user == storage.get(User, self.user.id))
        self.assertEqual(json_data['error'], 'Not found')


class DeleteUsersApiTest(unittest.TestCase):
    """
        Tests of API delete action for User.
    """

    def setUp(self) -> None:
        """
            Set up API delete action tests.
        """
        self.user = User(last_name='toto', first_name='titi',
                         email='email', password='password')
        self.user_id = self.user.id
        storage.new(self.user)
        storage.save()
        self.url = '{}/users/{}'.format(api_url, self.user.id)
        self.invalid_url = '{}/users/{}'.format(api_url, 'toto')

    def tearDown(self) -> None:
        """
            Tear down table User of database used for tests.
        """
        if storage.get(User, self.user.id) is not None:
            storage.delete(self.user)
            storage.save()

    def testDelete(self):
        """
            Test valid delete action.
        """
        response = requests.delete(url=self.url)
        headers = response.headers
        json_data = response.json()

        self.assertTrue(self.user == storage.get(User, self.user_id))
        self.assertEqual(response.status_code, 200, WRONG_STATUS_CODE_MSG)
        self.assertEqual(
            headers['Content-Type'], 'application/json', WRONG_TYPE_RETURN_MSG)
        self.assertEqual(len(json_data), 0)
        storage.reload()
        self.assertIsNone(storage.get(User, self.user_id))

    def testNotFound(self):
        """
            Test delete action when given wrong user_id or no ID at all.
        """
        response = requests.delete(url=self.invalid_url)
        headers = response.headers
        json_data = response.json()

        self.assertEqual(response.status_code, 404, WRONG_STATUS_CODE_MSG)
        self.assertEqual(
            headers['Content-Type'], 'application/json', WRONG_TYPE_RETURN_MSG)
        self.assertTrue(self.user == storage.get(User, self.user.id))
        self.assertIn('error', json_data.keys())
        self.assertEqual(json_data['error'], 'Not found')


class CreateUsersApiTest(unittest.TestCase):
    """
        Tests of API create action for User.
    """

    def setUp(self) -> None:
        """
            Set up API create action.
        """
        self.url = '{}/users/'.format(api_url)

    def testCreate(self):
        """
            Test valid create action tests.
        """
        data = {'last_name': 'toto', 'first_name': 'titi',
                'email': 'email', 'password': 'password'}
        response = requests.post(url=self.url, data=json.dumps(data))
        headers = response.headers

        self.assertEqual(response.status_code, 201, WRONG_STATUS_CODE_MSG)
        self.assertEqual(
            headers['Content-Type'], 'application/json', WRONG_TYPE_RETURN_MSG)
        json_data = response.json()
        user = storage.get(User, json_data['id'])
        self.assertIsInstance(user, User)
        self.assertIn('last_name', json_data, MISSING_LASTNAME_ATTR_MSG)
        self.assertIn('first_name', json_data, MISSING_FIRSTNAME_ATTR_MSG)
        self.assertIn('email', json_data, MISSING_EMAIL_ATTR_MSG)
        self.assertIn('password', json_data, MISSING_PASSWORD_ATTR_MSG)
        self.assertIn('created_at', json_data, MISSING_CREATED_AT_ATTR_MSG)
        self.assertIn('updated_at', json_data, MISSING_UPDATED_AT_ATTR_MSG)
        self.assertIn('__class__', json_data, MISSING_CLASS_ATTR_MSG)
        self.assertEqual(json_data['email'], 'email')
        self.assertEqual(json_data['password'], 'password')
        storage.delete(user)
        storage.save()

    def testMissingEmailAttribute(self):
        """
            Test create action when given dict without email key for user.
        """
        data = {'bidule': 'toto'}
        response = requests.post(url=self.url, data=json.dumps(data))
        headers = response.headers

        self.assertEqual(response.status_code, 400, WRONG_STATUS_CODE_MSG)
        self.assertEqual(
            headers['Content-Type'], 'text/html; charset=utf-8',
            WRONG_TYPE_RETURN_MSG)
        self.assertEqual(response.content, b'Missing email')

    def testMissingPasswordAttribute(self):
        """
            Test create action when given dict without password key for user.
        """
        data = {'email': 'email'}
        response = requests.post(url=self.url, data=json.dumps(data))
        headers = response.headers

        self.assertEqual(response.status_code, 400, WRONG_STATUS_CODE_MSG)
        self.assertEqual(
            headers['Content-Type'], 'text/html; charset=utf-8',
            WRONG_TYPE_RETURN_MSG)
        self.assertEqual(response.content, b'Missing password')

    def testNotAJson(self):
        """
            Test create action when given wrong data format.
        """
        data = {'email': 'email', 'password': 'password'}
        response = requests.post(url=self.url, data=data)
        headers = response.headers

        self.assertEqual(response.status_code, 400, WRONG_STATUS_CODE_MSG)
        self.assertEqual(
            headers['Content-Type'], 'text/html; charset=utf-8',
            WRONG_TYPE_RETURN_MSG)
        self.assertEqual(response.content, b'Not a JSON')


class UpdateUsersApiTest(unittest.TestCase):
    """
        Tests of API update action for User.
    """

    def setUp(self) -> None:
        """
            Set up API update action tests.
        """
        self.user = User(last_name='toto', first_name='titi',
                         email='email', password='password')
        self.user_id = self.user.id
        storage.new(self.user)
        storage.save()
        self.url = '{}/users/{}'.format(api_url, self.user_id)
        self.invalid_url = '{}/users/{}'.format(api_url, 'toto')

    def tearDown(self) -> None:
        """
            Tear down table User of database used for tests.
        """
        if storage.get(User, self.user.id) is not None:
            storage.delete(self.user)
            storage.save()

    def testUpdate(self):
        """
            Test valid update action.
        """
        data = {'last_name': 'toto2', 'first_name': 'titi',
                'email': 'email', 'password': 'password'}
        response = requests.put(url=self.url, data=json.dumps(data))
        headers = response.headers
        json_data = response.json()

        self.assertTrue(self.user == storage.get(User, self.user_id))
        self.assertEqual(response.status_code, 200, WRONG_STATUS_CODE_MSG)
        self.assertEqual(
            headers['Content-Type'], 'application/json', WRONG_TYPE_RETURN_MSG)
        storage.reload()
        user = storage.get(User, self.user_id)
        self.assertEqual(user.last_name, 'toto2')
        self.assertIn('last_name', json_data, MISSING_LASTNAME_ATTR_MSG)
        self.assertIn('first_name', json_data, MISSING_FIRSTNAME_ATTR_MSG)
        self.assertIn('email', json_data, MISSING_EMAIL_ATTR_MSG)
        self.assertIn('password', json_data, MISSING_PASSWORD_ATTR_MSG)
        self.assertIn('created_at', json_data, MISSING_CREATED_AT_ATTR_MSG)
        self.assertIn('updated_at', json_data, MISSING_UPDATED_AT_ATTR_MSG)
        self.assertIn('__class__', json_data, MISSING_CLASS_ATTR_MSG)
        self.assertEqual(json_data['last_name'], 'toto2')
        storage.delete(user)
        storage.save()

    def testNotAJson(self):
        """
            Test update action when given an invalid json.
        """
        data = {'last_name': 'toto2', 'first_name': 'titi',
                'email': 'email', 'password': 'password'}
        response = requests.put(url=self.url, data=data)
        headers = response.headers

        self.assertEqual(response.status_code, 400, WRONG_STATUS_CODE_MSG)
        self.assertEqual(
            headers['Content-Type'], 'text/html; charset=utf-8',
            WRONG_TYPE_RETURN_MSG)
        self.assertEqual(response.content, b'Not a JSON')

    def testNotFound(self):
        """
            Test update action when given a wrong ID.
        """
        data = {'last_name': 'toto2', 'first_name': 'titi',
                'email': 'email', 'password': 'password'}
        response = requests.put(url=self.invalid_url, data=json.dumps(data))
        headers = response.headers
        json_data = response.json()

        self.assertEqual(response.status_code, 404, WRONG_STATUS_CODE_MSG)
        self.assertEqual(
            headers['Content-Type'], 'application/json', WRONG_TYPE_RETURN_MSG)
        self.assertTrue(self.user == storage.get(User, self.user.id))
        self.assertEqual(json_data['error'], 'Not found')
