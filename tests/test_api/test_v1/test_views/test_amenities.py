#!/usr/bin/python3
import json
from models import storage
from models.amenity import Amenity
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


class ListAmenitiesApiTest(unittest.TestCase):
    """
        Tests of API list action for Amenity.
    """

    def setUp(self) -> None:
        """
            Set up API list action tests.
        """
        self.url = '{}/amenities'.format(api_url)

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
        initial_count = len(storage.all(Amenity))
        response = requests.get(url=self.url)
        json_data = response.json()

        self.assertEqual(initial_count, len(json_data))

    def testOnlyAmenity(self):
        """
            Test valid list action with Amenity content only.
        """
        state = State(name='toto')
        amenity = Amenity(name='toto')
        storage.new(state)
        storage.new(amenity)
        storage.save()

        response = requests.get(url=self.url)
        json_data = response.json()

        for element in json_data:
            self.assertEqual(element['__class__'], 'Amenity', WRONG_OBJ_TYPE_MSG)

        storage.delete(amenity)
        storage.delete(state)
        storage.save()
