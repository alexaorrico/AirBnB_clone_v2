#!/usr/bin/python3
import json
from models import storage
from models.state import State
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
MISSING_NAME_ATTR_MSG = 'Missing name!'
MISSING_CREATED_AT_ATTR_MSG = 'Missing created_at!'
MISSING_UPDATED_AT_ATTR_MSG = 'Missing updated_at!'
MISSING_CLASS_ATTR_MSG = 'Missing class!'


class ListStatesApiTest(unittest.TestCase):
    """
        Tests of API list action for State.
    """

    def setUp(self) -> None:
        """
            Set up API list action tests.
        """
        self.url = '{}/states'.format(api_url)

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
        initial_count = len(storage.all(State))
        response = requests.get(url=self.url)
        json_data = response.json()

        self.assertEqual(initial_count, len(json_data))

    def testOnlyState(self):
        """
            Test valid list action with State content only.
        """
        response = requests.get(url=self.url)
        json_data = response.json()

        for element in json_data:
            self.assertEqual(element['__class__'], 'State', WRONG_OBJ_TYPE_MSG)


class ShowStatesApiTest(unittest.TestCase):
    """
        Tests of API show action for State.
    """

    def setUp(self) -> None:
        """
            Set up API show action tests.
        """
        self.state = State(name='toto')
        storage.new(self.state)
        storage.save()
        self.url = '{}/states/{}'.format(api_url, self.state.id)
        self.invalid_url = '{}/states/{}'.format(api_url, 'toto')

    def tearDown(self) -> None:
        """
            Tear down table State of database used for tests.
        """
        storage.delete(self.state)
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
        self.assertIn('name', json_data)
        self.assertIn('created_at', json_data)
        self.assertIn('updated_at', json_data)
        self.assertIn('__class__', json_data)
        self.assertEqual(json_data['name'], self.state.name)

    def testNotFound(self):
        """
            Test show action when given wrong state_id or no ID at all.
        """
        response = requests.get(url=self.invalid_url)
        headers = response.headers
        json_data = response.json()

        self.assertEqual(response.status_code, 404, WRONG_STATUS_CODE_MSG)
        self.assertEqual(
            headers['Content-Type'], 'application/json', WRONG_TYPE_RETURN_MSG)
        self.assertTrue(self.state == storage.get(State, self.state.id))
        self.assertEqual(json_data['error'], 'Not found')


class DeleteStatesApiTest(unittest.TestCase):
    """
        Tests of API delete action for State.
    """

    def setUp(self) -> None:
        """
            Set up API delete action tests.
        """
        self.state = State(name='toto')
        self.state_id = self.state.id
        storage.new(self.state)
        storage.save()
        self.url = '{}/states/{}'.format(api_url, self.state.id)
        self.invalid_url = '{}/states/{}'.format(api_url, 'toto')

    def tearDown(self) -> None:
        """
            Tear down table State of database used for tests.
        """
        if storage.get(State, self.state.id) is not None:
            storage.delete(self.state)
            storage.save()

    def testDelete(self):
        """
            Test valid delete action.
        """
        response = requests.delete(url=self.url)
        headers = response.headers
        json_data = response.json()

        self.assertTrue(self.state == storage.get(State, self.state_id))
        self.assertEqual(response.status_code, 200, WRONG_STATUS_CODE_MSG)
        self.assertEqual(
            headers['Content-Type'], 'application/json', WRONG_TYPE_RETURN_MSG)
        self.assertEqual(len(json_data), 0)
        storage.reload()
        self.assertIsNone(storage.get(State, self.state_id))

    def testNotFound(self):
        """
            Test delete action when given wrong state_id or no ID at all.
        """
        response = requests.delete(url=self.invalid_url)
        headers = response.headers
        json_data = response.json()

        self.assertEqual(response.status_code, 404, WRONG_STATUS_CODE_MSG)
        self.assertEqual(
            headers['Content-Type'], 'application/json', WRONG_TYPE_RETURN_MSG)
        self.assertTrue(self.state == storage.get(State, self.state.id))
        self.assertEqual(json_data['error'], 'Not found')


class CreateStatesApiTest(unittest.TestCase):
    """
        Tests of API create action for State.
    """

    def setUp(self) -> None:
        """
            Set up API create action.
        """
        self.url = '{}/states/'.format(api_url)

    def testCreate(self):
        """
            Test valid create action tests.
        """
        data = {'name': 'toto'}
        response = requests.post(url=self.url, data=json.dumps(data))
        headers = response.headers

        self.assertEqual(response.status_code, 201, WRONG_STATUS_CODE_MSG)
        self.assertEqual(
            headers['Content-Type'], 'application/json', WRONG_TYPE_RETURN_MSG)
        json_data = response.json()
        state = storage.get(State, json_data['id'])
        self.assertIsInstance(storage.get(State, json_data['id']), State)
        self.assertIn('name', json_data, MISSING_NAME_ATTR_MSG)
        self.assertIn('created_at', json_data, MISSING_CREATED_AT_ATTR_MSG)
        self.assertIn('updated_at', json_data, MISSING_UPDATED_AT_ATTR_MSG)
        self.assertIn('__class__', json_data, MISSING_CLASS_ATTR_MSG)
        self.assertEqual(json_data['name'], 'toto')
        storage.delete(state)
        storage.save()

    def testMissingNameAttribute(self):
        """
            Test create action when given dict without name key for state.
        """
        data = {'bidule': 'toto'}
        response = requests.post(url=self.url, data=json.dumps(data))
        headers = response.headers

        self.assertEqual(response.status_code, 400, WRONG_STATUS_CODE_MSG)
        self.assertEqual(
            headers['Content-Type'], 'text/html; charset=utf-8',
            WRONG_TYPE_RETURN_MSG)
        self.assertEqual(response.content, b'Missing name')

    def testNotAJson(self):
        """
            Test create action when given wrong data format.
        """
        data = {'name': 'toto'}
        response = requests.post(url=self.url, data=data)
        headers = response.headers

        self.assertEqual(response.status_code, 400, WRONG_STATUS_CODE_MSG)
        self.assertEqual(
            headers['Content-Type'], 'text/html; charset=utf-8',
            WRONG_TYPE_RETURN_MSG)
        self.assertEqual(response.content, b'Not a JSON')


class UpdateStatesApiTest(unittest.TestCase):
    """
        Tests of API update action for State.
    """

    def setUp(self) -> None:
        """
            Set up API update action tests.
        """
        self.state = State(name='toto')
        self.state_id = self.state.id
        storage.new(self.state)
        storage.save()
        self.url = '{}/states/{}'.format(api_url, self.state_id)
        self.invalid_url = '{}/states/{}'.format(api_url, 'toto')

    def tearDown(self) -> None:
        """
            Tear down table State of database used for tests.
        """
        if storage.get(State, self.state.id) is not None:
            storage.delete(self.state)
            storage.save()

    def testUpdate(self):
        """
            Test valid update action.
        """
        data = {'name': 'toto2'}
        response = requests.put(url=self.url, data=json.dumps(data))
        headers = response.headers
        json_data = response.json()

        self.assertTrue(self.state == storage.get(State, self.state_id))
        self.assertEqual(response.status_code, 200, WRONG_STATUS_CODE_MSG)
        self.assertEqual(
            headers['Content-Type'], 'application/json', WRONG_TYPE_RETURN_MSG)
        storage.reload()
        state = storage.get(State, self.state_id)
        self.assertEqual(state.name, 'toto2')
        self.assertIn('name', json_data, MISSING_NAME_ATTR_MSG)
        self.assertIn('created_at', json_data, MISSING_CREATED_AT_ATTR_MSG)
        self.assertIn('updated_at', json_data, MISSING_UPDATED_AT_ATTR_MSG)
        self.assertIn('__class__', json_data, MISSING_CLASS_ATTR_MSG)
        self.assertEqual(json_data['name'], 'toto2')
        storage.delete(state)
        storage.save()

    def testNotAJson(self):
        """
            Test update action when given an invalid json.
        """
        data = {'name': 'toto'}
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
        data = {'name': 'toto'}
        response = requests.put(url=self.invalid_url, data=json.dumps(data))
        headers = response.headers
        json_data = response.json()

        self.assertEqual(response.status_code, 404, WRONG_STATUS_CODE_MSG)
        self.assertEqual(
            headers['Content-Type'], 'application/json', WRONG_TYPE_RETURN_MSG)
        self.assertTrue(self.state == storage.get(State, self.state.id))
        self.assertEqual(json_data['error'], 'Not found')
