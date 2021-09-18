#!/usr/bin/python3
import json
from models import storage
from models.state import State
from models.city import City
from models.place import Place
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
MISSING_NAME_ATTR_MSG = 'Missing name!'
MISSING_ROOM_NB_ATTR_MSG = 'Missing number_rooms!'
MISSING_BATHROOM_NB_ATTR_MSG = 'Missing number_bathrooms!'
MISSING_PRICE_BY_NIGHT_ATTR_MSG = 'Missing price_by_night!'
MISSING_USER_ID_ATTR_MSG = 'Missing user_id!'
MISSING_CITY_ID_ATTR_MSG = 'Missing city_id!'
MISSING_CREATED_AT_ATTR_MSG = 'Missing created_at!'
MISSING_UPDATED_AT_ATTR_MSG = 'Missing updated_at!'
MISSING_CLASS_ATTR_MSG = 'Missing class!'


class ListPlacesApiTest(unittest.TestCase):
    """
        Tests of API list action for Place.
    """

    def setUp(self) -> None:
        """
            Set up API list action tests.
        """
        self.state = State(name='toto')
        self.state_id = self.state.id
        self.city = City(name='toto', state_id=self.state_id)
        self.city_id = self.city.id
        self.user = User(email='email', password='password')
        self.user_id = self.user.id
        storage.new(self.state)
        storage.new(self.city)
        storage.new(self.user)
        storage.save()
        self.url = '{}/cities/{}/places'.format(api_url, self.city_id)
        self.invalid_url = '{}/cities/{}/places'.format(api_url, 'toto')

    def tearDown(self) -> None:
        """
            Tear down table Review of database used for tests.
        """
        user = storage.get(User, self.user_id)
        if user is not None:
            storage.delete(user)
        city = storage.get(City, self.city_id)
        if city is not None:
            storage.delete(city)
        state = storage.get(State, self.state_id)
        if state is not None:
            storage.delete(state)
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
        user = User(email='email', password='password')
        place = Place(name='toto', city_id=self.city_id, user_id=user.id)
        storage.new(user)
        storage.new(place)
        storage.save()
        obj_city = storage.get(City, self.city_id)
        initial_count = len(obj_city.places)
        response = requests.get(url=self.url)
        json_data = response.json()

        self.assertEqual(initial_count, len(json_data))

        storage.delete(place)
        storage.delete(user)
        storage.save()

    def testOnlyPlace(self):
        """
            Test valid list action with Place content only.
        """
        state = State(name='toto')
        city = City(name='toto', state_id=state.id)
        user = User(email='email', password='password')
        place = Place(name='toto', city_id=city.id, user_id=user.id)
        storage.new(state)
        storage.new(city)
        storage.new(user)
        storage.new(place)
        storage.save()
        response = requests.get(url=self.url)
        json_data = response.json()

        for element in json_data:
            self.assertEqual(element['__class__'], 'Place', WRONG_OBJ_TYPE_MSG)
        storage.delete(place)
        storage.delete(user)
        storage.delete(city)
        storage.delete(state)
        storage.save()

    def testNotFound(self):
        """
            Test create action when given wrong city_id or no ID at all.
        """
        response = requests.get(url=self.invalid_url)
        headers = response.headers
        json_data = response.json()

        self.assertEqual(response.status_code, 404, WRONG_STATUS_CODE_MSG)
        self.assertEqual(
            headers['Content-Type'], 'application/json', WRONG_TYPE_RETURN_MSG)
        self.assertTrue(self.city == storage.get(City, self.city_id))
        self.assertIn('error', json_data)
        self.assertEqual(json_data['error'], 'Not found')


class ShowPlacesApiTest(unittest.TestCase):
    """
        Tests of API show action for Place.
    """

    def setUp(self) -> None:
        """
            Set up API show action tests.
        """
        self.state = State(name='toto')
        self.state_id = self.state.id
        self.city = City(name='toto', state_id=self.state.id)
        self.city_id = self.city.id
        self.user = User(email='email', password='password')
        self.user_id = self.user.id
        self.place = Place(name='toto', city_id=self.city.id,
                           user_id=self.user.id)
        self.place_id = self.place.id
        storage.new(self.state)
        storage.new(self.city)
        storage.new(self.user)
        storage.new(self.place)
        storage.save()
        self.url = '{}/places/{}'.format(api_url, self.place.id)
        self.invalid_url = '{}/places/{}'.format(api_url, 'toto')

    def tearDown(self) -> None:
        """
            Tear down table Place of database used for tests.
        """
        storage.delete(self.place)
        storage.delete(self.user)
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
        self.assertIn('name', json_data, MISSING_NAME_ATTR_MSG)
        self.assertIn('number_rooms', json_data, MISSING_ROOM_NB_ATTR_MSG)
        self.assertIn('number_bathrooms', json_data,
                      MISSING_BATHROOM_NB_ATTR_MSG)
        self.assertIn('price_by_night', json_data,
                      MISSING_PRICE_BY_NIGHT_ATTR_MSG)
        self.assertIn('user_id', json_data, MISSING_USER_ID_ATTR_MSG)
        self.assertIn('city_id', json_data, MISSING_CITY_ID_ATTR_MSG)
        self.assertIn('created_at', json_data, MISSING_CREATED_AT_ATTR_MSG)
        self.assertIn('updated_at', json_data, MISSING_UPDATED_AT_ATTR_MSG)
        self.assertIn('__class__', json_data, MISSING_CLASS_ATTR_MSG)
        self.assertEqual(json_data['name'], self.place.name)
        self.assertEqual(json_data['number_rooms'], self.place.number_rooms)
        self.assertEqual(json_data['number_bathrooms'],
                         self.place.number_bathrooms)
        self.assertEqual(json_data['price_by_night'],
                         self.place.price_by_night)
        self.assertEqual(json_data['user_id'], self.place.user_id)
        self.assertEqual(json_data['city_id'], self.place.city_id)

    def testNotFound(self):
        """
            Test show action when given wrong place_id or no ID at all.
        """
        response = requests.get(url=self.invalid_url)
        headers = response.headers
        json_data = response.json()

        self.assertEqual(response.status_code, 404, WRONG_STATUS_CODE_MSG)
        self.assertEqual(
            headers['Content-Type'], 'application/json', WRONG_TYPE_RETURN_MSG)
        self.assertTrue(self.place == storage.get(Place, self.place.id))
        self.assertEqual(json_data['error'], 'Not found')


class DeletePlacesApiTest(unittest.TestCase):
    """
        Tests of API delete action for Place.
    """

    def setUp(self) -> None:
        """
            Set up API show action tests.
        """
        self.state = State(name='toto')
        self.state_id = self.state.id
        self.city = City(name='toto', state_id=self.state.id)
        self.city_id = self.city.id
        self.user = User(email='email', password='password')
        self.user_id = self.user.id
        self.place = Place(name='toto', city_id=self.city.id,
                           user_id=self.user.id)
        self.place_id = self.place.id
        storage.new(self.state)
        storage.new(self.city)
        storage.new(self.user)
        storage.new(self.place)
        storage.save()
        self.url = '{}/places/{}'.format(api_url, self.place.id)
        self.invalid_url = '{}/places/{}'.format(api_url, 'toto')

    def tearDown(self) -> None:
        """
            Tear down table Place of database used for tests.
        """
        place = storage.get(Place, self.place_id)
        if place is not None:
            storage.delete(place)
        user = storage.get(User, self.user_id)
        if user is not None:
            storage.delete(user)
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

        self.assertTrue(self.place == storage.get(Place, self.place_id))
        self.assertTrue(self.user == storage.get(User, self.user_id))
        self.assertTrue(self.city == storage.get(City, self.city_id))
        self.assertTrue(self.state == storage.get(State, self.state_id))
        self.assertEqual(response.status_code, 200, WRONG_STATUS_CODE_MSG)
        self.assertEqual(
            headers['Content-Type'], 'application/json', WRONG_TYPE_RETURN_MSG)
        self.assertEqual(len(json_data), 0)
        storage.reload()
        self.assertIsNone(storage.get(Place, self.place_id))

    def testNotFound(self):
        """
            Test delete action when given wrong place_id or no ID at all.
        """
        response = requests.delete(url=self.invalid_url)
        headers = response.headers
        json_data = response.json()

        self.assertEqual(response.status_code, 404, WRONG_STATUS_CODE_MSG)
        self.assertEqual(
            headers['Content-Type'], 'application/json', WRONG_TYPE_RETURN_MSG)
        self.assertTrue(self.place == storage.get(Place, self.place.id))
        self.assertIn('error', json_data.keys())
        self.assertEqual(json_data['error'], 'Not found')


class CreatePlacesApiTest(unittest.TestCase):
    """
        Tests of API create action for Place.
    """

    def setUp(self) -> None:
        """
            Set up API create action.
        """
        self.state = State(name='toto')
        self.state_id = self.state.id
        self.city = City(name='toto', state_id=self.state_id)
        self.city_id = self.city.id
        self.user = User(email='email', password='password')
        self.user_id = self.user.id
        storage.new(self.state)
        storage.new(self.city)
        storage.new(self.user)
        storage.save()
        self.url = '{}/cities/{}/places/'.format(api_url, self.city_id)
        self.invalid_url = '{}/cities/{}/places'.format(api_url, 'toto')

    def tearDown(self) -> None:
        """
            Tear down table Place of database used for tests.
        """
        user = storage.get(User, self.user_id)
        if user is not None:
            storage.delete(user)
        city = storage.get(City, self.city_id)
        if city is not None:
            storage.delete(city)
        state = storage.get(State, self.state_id)
        if state is not None:
            storage.delete(state)
        storage.save()

    def testCreate(self):
        """
            Test valid create action tests.
        """
        self.assertTrue(self.user == storage.get(User, self.user_id))
        data = {'name': 'toto', 'user_id': self.user_id}
        response = requests.post(url=self.url, data=json.dumps(data))
        headers = response.headers

        self.assertEqual(response.status_code, 201, WRONG_STATUS_CODE_MSG)
        self.assertEqual(
            headers['Content-Type'], 'application/json', WRONG_TYPE_RETURN_MSG)
        json_data = response.json()
        place = storage.get(Place, json_data['id'])
        self.assertIsInstance(storage.get(Place, json_data['id']), Place)
        self.assertIn('name', json_data, MISSING_NAME_ATTR_MSG)
        self.assertIn('number_rooms', json_data, MISSING_ROOM_NB_ATTR_MSG)
        self.assertIn('number_bathrooms', json_data,
                      MISSING_BATHROOM_NB_ATTR_MSG)
        self.assertIn('price_by_night', json_data,
                      MISSING_PRICE_BY_NIGHT_ATTR_MSG)
        self.assertIn('user_id', json_data, MISSING_USER_ID_ATTR_MSG)
        self.assertIn('city_id', json_data, MISSING_CITY_ID_ATTR_MSG)
        self.assertIn('created_at', json_data, MISSING_CREATED_AT_ATTR_MSG)
        self.assertIn('updated_at', json_data, MISSING_UPDATED_AT_ATTR_MSG)
        self.assertIn('__class__', json_data, MISSING_CLASS_ATTR_MSG)
        self.assertEqual(json_data['name'], 'toto')
        self.assertEqual(json_data['user_id'], self.user_id)
        storage.delete(place)
        storage.save()

    def testMissingNameAttribute(self):
        """
            Test create action when given dict without name key for user.
        """
        data = {'bidule': 'toto'}
        response = requests.post(url=self.url, data=json.dumps(data))
        headers = response.headers

        self.assertEqual(response.status_code, 400, WRONG_STATUS_CODE_MSG)
        self.assertEqual(
            headers['Content-Type'], 'text/html; charset=utf-8',
            WRONG_TYPE_RETURN_MSG)
        self.assertEqual(response.content, b'Missing name')

    def testMissingUserIdAttribute(self):
        """
            Test create action when given dict without user_id key for user.
        """
        data = {'name': 'toto'}
        response = requests.post(url=self.url, data=json.dumps(data))
        headers = response.headers

        self.assertEqual(response.status_code, 400, WRONG_STATUS_CODE_MSG)
        self.assertEqual(
            headers['Content-Type'], 'text/html; charset=utf-8',
            WRONG_TYPE_RETURN_MSG)
        self.assertEqual(response.content, b'Missing user_id')

    def testNotAJson(self):
        """
            # Test create action when given wrong data format.
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
        self.assertTrue(self.city == storage.get(City, self.city_id))
        self.assertIn('error', json_data)
        self.assertEqual(json_data['error'], 'Not found')


class UpdatePlacesApiTest(unittest.TestCase):
    """
        Tests of API update action for Place.
    """

    def setUp(self) -> None:
        """
            Set up API create action.
        """
        self.state = State(name='toto')
        self.state_id = self.state.id
        self.city = City(name='toto', state_id=self.state_id)
        self.city_id = self.city.id
        self.user = User(email='email', password='password')
        self.user_id = self.user.id
        self.place = Place(name='toto', city_id=self.city.id,
                           user_id=self.user.id)
        self.place_id = self.place.id
        storage.new(self.state)
        storage.new(self.city)
        storage.new(self.user)
        storage.new(self.place)
        storage.save()
        self.url = '{}/places/{}'.format(api_url, self.place_id)
        self.invalid_url = '{}/places/{}'.format(api_url, 'toto')

    def tearDown(self) -> None:
        """
            Tear down table Place of database used for tests.
        """
        place = storage.get(Place, self.place_id)
        if place is not None:
            storage.delete(place)
        user = storage.get(User, self.user_id)
        if user is not None:
            storage.delete(user)
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

        self.assertTrue(self.place == storage.get(Place, self.place_id))
        self.assertEqual(response.status_code, 200, WRONG_STATUS_CODE_MSG)
        self.assertEqual(
            headers['Content-Type'], 'application/json', WRONG_TYPE_RETURN_MSG)
        storage.reload()
        place = storage.get(Place, self.place_id)
        self.assertEqual(place.name, 'toto2')
        self.assertIn('name', json_data, MISSING_NAME_ATTR_MSG)
        self.assertIn('number_rooms', json_data, MISSING_ROOM_NB_ATTR_MSG)
        self.assertIn('number_bathrooms', json_data,
                      MISSING_BATHROOM_NB_ATTR_MSG)
        self.assertIn('price_by_night', json_data,
                      MISSING_PRICE_BY_NIGHT_ATTR_MSG)
        self.assertIn('user_id', json_data, MISSING_USER_ID_ATTR_MSG)
        self.assertIn('city_id', json_data, MISSING_CITY_ID_ATTR_MSG)
        self.assertIn('created_at', json_data, MISSING_CREATED_AT_ATTR_MSG)
        self.assertIn('updated_at', json_data, MISSING_UPDATED_AT_ATTR_MSG)
        self.assertIn('__class__', json_data, MISSING_CLASS_ATTR_MSG)
        self.assertEqual(json_data['name'], 'toto2')
        storage.delete(place)
        storage.save()

    def testNotAJson(self):
        """
            # Test update action when given wrong data format.
        """
        data = {'text': 'toto'}
        response = requests.put(url=self.url, data=data)
        headers = response.headers

        self.assertEqual(response.status_code, 400, WRONG_STATUS_CODE_MSG)
        self.assertEqual(
            headers['Content-Type'], 'text/html; charset=utf-8',
            WRONG_TYPE_RETURN_MSG)
        self.assertEqual(response.content, b'Not a JSON')

    def testNotFound(self):
        """
            Test update action when given wrong review_id or no ID at all.
        """
        data = {'text': 'toto'}
        response = requests.put(url=self.invalid_url, data=json.dumps(data))
        headers = response.headers
        json_data = response.json()

        self.assertEqual(response.status_code, 404, WRONG_STATUS_CODE_MSG)
        self.assertEqual(
            headers['Content-Type'], 'application/json', WRONG_TYPE_RETURN_MSG)
        self.assertIn('error', json_data)
        self.assertEqual(json_data['error'], 'Not found')
