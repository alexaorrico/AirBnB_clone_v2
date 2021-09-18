#!/usr/bin/python3
import json
from models import storage
from models.state import State
from models.city import City
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
MISSING_STATE_ID_ATTR_MSG = 'Missing state id'


class ListCitiesApiTest(unittest.TestCase):
    """
        Tests of API list action for City.
    """

    def setUp(self) -> None:
        """
            Set up API list action tests.
        """
        self.state = State(name='toto')
        storage.new(self.state)
        storage.save()
        self.url = '{}/states/{}/cities'.format(api_url, self.state.id)
        self.invalid_url = '{}/states/{}/cities'.format(api_url, 'toto')

    def tearDown(self) -> None:
        """
            Tear down table State & City of database used for tests.
        """
        storage.delete(self.state)
        storage.save()

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
        state_id = self.state.id
        city = City(name='totoCity', state_id=state_id)
        storage.new(city)
        storage.save()
        obj_state = storage.get(State, state_id)
        initial_count = len(obj_state.cities)
        response = requests.get(url=self.url)
        json_data = response.json()

        self.assertEqual(initial_count, len(json_data))

        storage.delete(city)
        storage.save()

    def testOnlyCity(self):
        """
            Test valid list action with City content only.
        """
        state = State(name='toto')
        state_id = self.state.id
        city = City(name='totoCity', state_id=state_id)
        storage.new(state)
        storage.new(city)
        storage.save()

        response = requests.get(url=self.url)
        json_data = response.json()

        for element in json_data:
            self.assertEqual(element['__class__'], 'City', WRONG_OBJ_TYPE_MSG)

        storage.delete(city)
        storage.delete(state)
        storage.save()

    def testNotFound(self):
        """
            Test list action when given wrong state_id.
        """
        response = requests.get(url=self.invalid_url)
        headers = response.headers
        json_data = response.json()

        self.assertEqual(response.status_code, 404, WRONG_STATUS_CODE_MSG)
        self.assertEqual(headers['Content-Type'],
                         'application/json', WRONG_TYPE_RETURN_MSG)
        self.assertIn('error', json_data.keys())
        self.assertEqual('Not found', json_data['error'])


class ShowCitiesApiTest(unittest.TestCase):
    """
        Tests of API show action for City.
    """

    def setUp(self) -> None:
        """
            Set up API show action tests.
        """
        self.state = State(name='toto')
        storage.new(self.state)
        storage.save()
        self.city = City(name='totoCity', state_id=self.state.id)
        storage.new(self.city)
        storage.save()
        self.url = '{}/cities/{}'.format(api_url, self.city.id)
        self.invalid_url = '{}/cities/{}'.format(api_url, 'toto')

    def tearDown(self) -> None:
        """
            Tear down table State & City of database used for tests.
        """
        storage.delete(self.city)
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
        self.assertEqual(json_data['name'], self.city.name)

    def testNotFound(self):
        """
            Test show action when given wrong city_id.
        """
        response = requests.get(url=self.invalid_url)
        headers = response.headers
        json_data = response.json()

        self.assertEqual(response.status_code, 404, WRONG_STATUS_CODE_MSG)
        self.assertEqual(headers['Content-Type'],
                         'application/json', WRONG_TYPE_RETURN_MSG)
        self.assertIn('error', json_data.keys())
        self.assertEqual('Not found', json_data['error'])


class DeleteCitiesApiTest(unittest.TestCase):
    """
        Tests of API delete action for City.
    """

    def setUp(self) -> None:
        """
            Set up API delete action tests.
        """
        self.state = State(name='toto')
        storage.new(self.state)
        storage.save()
        self.state_id = self.state.id
        self.city = City(name='totoCity', state_id=self.state_id)
        storage.new(self.city)
        storage.save()
        self.city_id = self.city.id
        self.url = '{}/cities/{}'.format(api_url, self.city.id)
        self.invalid_url = '{}/cities/{}'.format(api_url, 'toto')

    def tearDown(self) -> None:
        """
            Tear down table State & City of database used for tests.
        """
        city = storage.get(City, self.city_id)
        if city is not None:
            storage.delete(city)
        state = storage.get(State, self.state_id)
        if state is not None:
            storage.delete(state)
        storage.save()

    def testDelete(self):
        """
            Test valid delete action.
        """
        response = requests.delete(url=self.url)
        headers = response.headers
        json_data = response.json()

        self.assertTrue(self.city == storage.get(City, self.city_id))
        self.assertTrue(self.state == storage.get(State, self.state_id))
        self.assertEqual(self.city.state_id, self.state.id)
        self.assertEqual(response.status_code, 200, WRONG_STATUS_CODE_MSG)
        self.assertEqual(
            headers['Content-Type'], 'application/json', WRONG_TYPE_RETURN_MSG)
        self.assertEqual(len(json_data), 0)
        storage.reload()
        self.assertIsNone(storage.get(City, self.city_id))

    def testNotFound(self):
        """
            Test delete action when given wrong city_id or no ID at all.
        """
        response = requests.delete(url=self.invalid_url)
        headers = response.headers
        json_data = response.json()

        self.assertEqual(response.status_code, 404, WRONG_STATUS_CODE_MSG)
        self.assertEqual(
            headers['Content-Type'], 'application/json', WRONG_TYPE_RETURN_MSG)
        self.assertTrue(self.state == storage.get(State, self.state.id))
        self.assertEqual(json_data['error'], 'Not found')


class CreateCitiesApiTest(unittest.TestCase):
    """
        Tests of API create action for City.
    """

    def setUp(self) -> None:
        """
            Set up API create action.
        """
        self.state = State(name='toto')
        storage.new(self.state)
        storage.save()
        self.state_id = self.state.id
        self.url = '{}/states/{}/cities'.format(api_url, self.state_id)
        self.invalid_url = '{}/states/{}/cities'.format(api_url, 'toto')

    def tearDown(self) -> None:
        state = storage.get(State, self.state_id)
        if state is not None:
            storage.delete(state)
        storage.save()

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
        city = storage.get(City, json_data['id'])
        self.assertIsInstance(city, City)
        self.assertIn('name', json_data, MISSING_NAME_ATTR_MSG)
        self.assertIn('created_at', json_data, MISSING_CREATED_AT_ATTR_MSG)
        self.assertIn('updated_at', json_data, MISSING_UPDATED_AT_ATTR_MSG)
        self.assertIn('__class__', json_data, MISSING_CLASS_ATTR_MSG)
        self.assertIn('state_id', json_data, MISSING_STATE_ID_ATTR_MSG)
        self.assertEqual(json_data['name'], 'toto')
        storage.delete(city)
        storage.save()

    def testMissingNameAttribute(self):
        """
            Test create action when given dict without name key for city.
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

    def testNotFound(self):
        """
            Test create action when given wrong city_id or no ID at all.
        """
        response = requests.post(url=self.invalid_url)
        headers = response.headers
        json_data = response.json()

        self.assertEqual(response.status_code, 404, WRONG_STATUS_CODE_MSG)
        self.assertEqual(
            headers['Content-Type'], 'application/json', WRONG_TYPE_RETURN_MSG)
        self.assertTrue(self.state == storage.get(State, self.state_id))
        self.assertIn('error', json_data)
        self.assertEqual(json_data['error'], 'Not found')


class UpdateCitiesApiTest(unittest.TestCase):
    """
        Tests of API update action for City
    """

    def setUp(self) -> None:
        """
            Set up API update action tests.
        """
        self.state = State(name='toto')
        storage.new(self.state)
        storage.save()
        self.state_id = self.state.id
        self.city = City(name='totoCity', state_id=self.state_id)
        storage.new(self.city)
        storage.save()
        self.city_id = self.city.id
        self.url = '{}/cities/{}'.format(api_url, self.city.id)
        self.invalid_url = '{}/cities/{}'.format(api_url, 'toto')

    def tearDown(self) -> None:
        """
            Tear down table State & City of database used for tests.
        """
        city = storage.get(City, self.city_id)
        if city is not None:
            storage.delete(city)
        state = storage.get(State, self.state_id)
        if state is not None:
            storage.delete(state)
        storage.save()

    def testUpdate(self):
        """
            Test valid update action.
        """
        data = {'name': 'toto2'}
        response = requests.put(url=self.url, data=json.dumps(data))
        headers = response.headers
        json_data = response.json()

        self.assertTrue(self.city == storage.get(City, self.city_id))
        self.assertEqual(response.status_code, 200, WRONG_STATUS_CODE_MSG)
        self.assertEqual(
            headers['Content-Type'], 'application/json', WRONG_TYPE_RETURN_MSG)
        storage.reload()
        city = storage.get(City, self.city_id)
        self.assertEqual(city.name, 'toto2')
        self.assertIn('name', json_data, MISSING_NAME_ATTR_MSG)
        self.assertIn('created_at', json_data, MISSING_CREATED_AT_ATTR_MSG)
        self.assertIn('updated_at', json_data, MISSING_UPDATED_AT_ATTR_MSG)
        self.assertIn('__class__', json_data, MISSING_CLASS_ATTR_MSG)
        self.assertIn('state_id', json_data, MISSING_STATE_ID_ATTR_MSG)
        self.assertEqual(json_data['name'], 'toto2')
        storage.delete(city)
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
            Test update action when given wrong city_id or no ID at all.
        """
        response = requests.delete(url=self.invalid_url)
        headers = response.headers
        json_data = response.json()

        self.assertEqual(response.status_code, 404, WRONG_STATUS_CODE_MSG)
        self.assertEqual(
            headers['Content-Type'], 'application/json', WRONG_TYPE_RETURN_MSG)
        self.assertTrue(self.state == storage.get(State, self.state.id))
        self.assertEqual(json_data['error'], 'Not found')
