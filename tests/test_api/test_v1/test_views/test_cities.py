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
        initial_count = len(storage.all(State.cities))
        response = requests.get(url=self.url)
        json_data = response.json()

        self.assertEqual(initial_count, len(json_data))

    def testOnlyCity(self):
        """
            Test valid list action with City content only.
        """
        response = requests.get(url=self.url)
        json_data = response.json()

        for element in json_data:
            self.assertEqual(element['__class__'], 'City', WRONG_OBJ_TYPE_MSG)

    def testNotFound(self):
        """

        """
        response = requests.get(url=self.invalid_url)
        headers = response.headers
        json_data = response.json()

        self.assertEqual(response.status_code, 404, WRONG_STATUS_CODE_MSG)
        self.assertEqual(headers['Content-Type'],
                         'application/json', WRONG_TYPE_RETURN_MSG)
        self.assertIn('error', json_data.keys())
        self.assertEqual('Not found', json_data['error'])
