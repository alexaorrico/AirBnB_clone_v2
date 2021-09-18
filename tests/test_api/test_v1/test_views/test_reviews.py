#!/usr/bin/python3
import json
from models import storage
from models.city import City
from models.place import Place
from models.review import Review
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
MISSING_TEXT_ATTR_MSG = 'Missing text!'
MISSING_USER_ID_ATTR_MSG = 'Missing user_id!'
MISSING_PLACE_ID_ATTR_MSG = 'Missing place_id!'
MISSING_CREATED_AT_ATTR_MSG = 'Missing created_at!'
MISSING_UPDATED_AT_ATTR_MSG = 'Missing updated_at!'
MISSING_CLASS_ATTR_MSG = 'Missing class!'


class ListReviewsApiTest(unittest.TestCase):
    """
        Tests of API list action for Review.
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
        self.place = Place(name='toto', city_id=self.city_id,
                           user_id=self.user_id)
        self.place_id = self.place.id
        storage.new(self.state)
        storage.new(self.city)
        storage.new(self.user)
        storage.new(self.place)
        storage.save()
        self.url = '{}/places/{}/reviews'.format(api_url, self.place_id)
        self.invalid_url = '{}/places/{}/reviews'.format(api_url, 'toto')

    def tearDown(self) -> None:
        """
            Tear down table Review of database used for tests.
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
        """
            Test list length.
        """
        user = User(email='email', password='password')
        review = Review(place_id=self.place_id, user_id=user.id, text='toto')
        storage.new(user)
        storage.new(review)
        storage.save()
        obj_place = storage.get(Place, self.place_id)
        initial_count = len(obj_place.reviews)
        response = requests.get(url=self.url)
        json_data = response.json()

        self.assertEqual(initial_count, len(json_data))

        storage.delete(review)
        storage.delete(user)
        storage.save()

    def testOnlyReview(self):
        """
            Test valid list action with Review content only.
        """
        user = User(email='email', password='password')
        review = Review(place_id=self.place_id, user_id=user.id, text='toto')
        storage.new(review)
        storage.new(user)
        storage.save()
        response = requests.get(url=self.url)
        json_data = response.json()

        for element in json_data:
            self.assertEqual(element['__class__'],
                             'Review', WRONG_OBJ_TYPE_MSG)
        storage.delete(review)
        storage.delete(user)
        storage.save()

    def testNotFound(self):
        """
            Test create action when given wrong place_id or no ID at all.
        """
        response = requests.get(url=self.invalid_url)
        headers = response.headers
        json_data = response.json()

        self.assertEqual(response.status_code, 404, WRONG_STATUS_CODE_MSG)
        self.assertEqual(
            headers['Content-Type'], 'application/json', WRONG_TYPE_RETURN_MSG)
        self.assertTrue(self.place == storage.get(Place, self.place_id))
        self.assertIn('error', json_data)
        self.assertEqual(json_data['error'], 'Not found')


class ShowReviewsApiTest(unittest.TestCase):
    """
        Tests of API show action for Review.
    """

    def setUp(self) -> None:
        """
            Set up API show action tests.
        """
        self.state = State(name='toto')
        self.state_id = self.state.id
        self.city = City(name='toto', state_id=self.state_id)
        self.city_id = self.city.id
        self.user = User(email='email', password='password')
        self.user_id = self.user.id
        self.place = Place(name='toto', city_id=self.city_id,
                           user_id=self.user_id)
        self.place_id = self.place.id
        self.review = Review(place_id=self.place_id,
                             user_id=self.user_id, text='blabla')
        self.review_id = self.review.id
        storage.new(self.state)
        storage.new(self.city)
        storage.new(self.user)
        storage.new(self.place)
        storage.new(self.review)
        storage.save()
        self.url = '{}/reviews/{}'.format(api_url, self.review_id)
        self.invalid_url = '{}/reviews/{}'.format(api_url, 'toto')

    def tearDown(self) -> None:
        """
            Tear down table Place of database used for tests.
        """
        review = storage.get(Review, self.review_id)
        if review is not None:
            storage.delete(review)
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
        self.assertIn('text', json_data, MISSING_TEXT_ATTR_MSG)
        self.assertIn('user_id', json_data, MISSING_USER_ID_ATTR_MSG)
        self.assertIn('place_id', json_data, MISSING_PLACE_ID_ATTR_MSG)
        self.assertIn('created_at', json_data, MISSING_CREATED_AT_ATTR_MSG)
        self.assertIn('updated_at', json_data, MISSING_UPDATED_AT_ATTR_MSG)
        self.assertIn('__class__', json_data, MISSING_CLASS_ATTR_MSG)
        self.assertEqual(json_data['text'], self.review.text)
        self.assertEqual(json_data['user_id'], self.review.user_id)
        self.assertEqual(json_data['place_id'], self.review.place_id)

    def testNotFound(self):
        """
            Test show action when given wrong review_id or no ID at all.
        """
        response = requests.get(url=self.invalid_url)
        headers = response.headers
        json_data = response.json()

        self.assertEqual(response.status_code, 404, WRONG_STATUS_CODE_MSG)
        self.assertEqual(
            headers['Content-Type'], 'application/json', WRONG_TYPE_RETURN_MSG)
        self.assertTrue(self.review == storage.get(Review, self.review_id))
        self.assertIn('error', json_data)
        self.assertEqual(json_data['error'], 'Not found')


class DeleteReviewsApiTest(unittest.TestCase):
    """
        Tests of API delete action for Review.
    """

    def setUp(self) -> None:
        """
            Set up API show action tests.
        """
        self.state = State(name='toto')
        self.state_id = self.state.id
        self.city = City(name='toto', state_id=self.state_id)
        self.city_id = self.city.id
        self.user = User(email='email', password='password')
        self.user_id = self.user.id
        self.place = Place(name='toto', city_id=self.city_id,
                           user_id=self.user_id)
        self.place_id = self.place.id
        self.review = Review(place_id=self.place_id,
                             user_id=self.user_id, text='blabla')
        self.review_id = self.review.id
        storage.new(self.state)
        storage.new(self.city)
        storage.new(self.user)
        storage.new(self.place)
        storage.new(self.review)
        storage.save()
        self.url = '{}/reviews/{}'.format(api_url, self.review_id)
        self.invalid_url = '{}/reviews/{}'.format(api_url, 'toto')

    def tearDown(self) -> None:
        """
            Tear down table Place of database used for tests.
        """
        review = storage.get(Review, self.review_id)
        if review is not None:
            storage.delete(review)
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

        self.assertTrue(self.review == storage.get(Review, self.review_id))
        self.assertTrue(self.place == storage.get(Place, self.place_id))
        self.assertTrue(self.user == storage.get(User, self.user_id))
        self.assertTrue(self.city == storage.get(City, self.city_id))
        self.assertTrue(self.state == storage.get(State, self.state_id))
        self.assertEqual(response.status_code, 200, WRONG_STATUS_CODE_MSG)
        self.assertEqual(
            headers['Content-Type'], 'application/json', WRONG_TYPE_RETURN_MSG)
        self.assertEqual(len(json_data), 0)
        storage.reload()
        self.assertIsNone(storage.get(Review, self.review_id))

    def testNotFound(self):
        """
            Test delete action when given wrong review_id or no ID at all.
        """
        response = requests.get(url=self.invalid_url)
        headers = response.headers
        json_data = response.json()

        self.assertEqual(response.status_code, 404, WRONG_STATUS_CODE_MSG)
        self.assertEqual(
            headers['Content-Type'], 'application/json', WRONG_TYPE_RETURN_MSG)
        self.assertTrue(self.review == storage.get(Review, self.review_id))
        self.assertIn('error', json_data)
        self.assertEqual(json_data['error'], 'Not found')


class CreateReviewsApiTest(unittest.TestCase):
    """
        Tests of API create action for Review.
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
        self.place = Place(name='toto', city_id=self.city_id,
                           user_id=self.user_id)
        self.place_id = self.place.id
        storage.new(self.state)
        storage.new(self.city)
        storage.new(self.user)
        storage.new(self.place)
        storage.save()
        self.url = '{}/places/{}/reviews'.format(api_url, self.place_id)
        self.invalid_url = '{}/places/{}/reviews'.format(api_url, 'toto')

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

    def testCreate(self):
        """
            Test valid create action tests.
        """
        self.assertTrue(self.user == storage.get(User, self.user_id))
        self.assertTrue(self.place == storage.get(Place, self.place_id))
        data = {'text': 'toto', 'user_id': self.user_id,
                'place_id': self.place_id}
        response = requests.post(url=self.url, data=json.dumps(data))
        headers = response.headers

        self.assertEqual(response.status_code, 201, WRONG_STATUS_CODE_MSG)
        self.assertEqual(
            headers['Content-Type'], 'application/json', WRONG_TYPE_RETURN_MSG)
        json_data = response.json()
        review = storage.get(Review, json_data['id'])
        self.assertIsInstance(storage.get(Review, json_data['id']), Review)
        self.assertIn('user_id', json_data, MISSING_USER_ID_ATTR_MSG)
        self.assertIn('place_id', json_data, MISSING_PLACE_ID_ATTR_MSG)
        self.assertIn('text', json_data, MISSING_TEXT_ATTR_MSG)
        self.assertIn('created_at', json_data, MISSING_CREATED_AT_ATTR_MSG)
        self.assertIn('updated_at', json_data, MISSING_UPDATED_AT_ATTR_MSG)
        self.assertIn('__class__', json_data, MISSING_CLASS_ATTR_MSG)
        self.assertEqual(json_data['user_id'], self.user_id)
        self.assertEqual(json_data['place_id'], self.place_id)
        self.assertEqual(json_data['text'], review.text)
        storage.delete(review)
        storage.save()

    def testMissingUserIdAttribute(self):
        """
            Test create action when given dict without user_id key for user.
        """
        data = {'bidule': 'toto'}
        response = requests.post(url=self.url, data=json.dumps(data))
        headers = response.headers

        self.assertEqual(response.status_code, 400, WRONG_STATUS_CODE_MSG)
        self.assertEqual(
            headers['Content-Type'], 'text/html; charset=utf-8',
            WRONG_TYPE_RETURN_MSG)
        self.assertEqual(response.content, b'Missing user_id')

    def testMissingTextAttribute(self):
        """
            Test create action when given dict without text key for user.
        """
        data = {'user_id': self.user_id}
        response = requests.post(url=self.url, data=json.dumps(data))
        headers = response.headers

        self.assertEqual(response.status_code, 400, WRONG_STATUS_CODE_MSG)
        self.assertEqual(
            headers['Content-Type'], 'text/html; charset=utf-8',
            WRONG_TYPE_RETURN_MSG)
        self.assertEqual(response.content, b'Missing text')

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
            Test create action when given wrong place_id or no ID at all.
        """
        response = requests.post(url=self.invalid_url)
        headers = response.headers
        json_data = response.json()

        self.assertEqual(response.status_code, 404, WRONG_STATUS_CODE_MSG)
        self.assertEqual(
            headers['Content-Type'], 'application/json', WRONG_TYPE_RETURN_MSG)
        self.assertTrue(self.place == storage.get(Place, self.place_id))
        self.assertIn('error', json_data)
        self.assertEqual(json_data['error'], 'Not found')


class UpdateReviewApiTest(unittest.TestCase):
    """
        Tests of API update action for Review.
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
        self.place = Place(name='toto', city_id=self.city_id,
                           user_id=self.user_id)
        self.place_id = self.place.id
        self.review = Review(place_id=self.place_id,
                             user_id=self.user_id, text='blabla')
        self.review_id = self.review.id
        storage.new(self.state)
        storage.new(self.city)
        storage.new(self.user)
        storage.new(self.place)
        storage.new(self.review)
        storage.save()
        self.url = '{}/reviews/{}'.format(api_url, self.review_id)
        self.invalid_url = '{}/reviews/{}'.format(api_url, 'toto')

    def tearDown(self) -> None:
        """
            Tear down table Place of database used for tests.
        """
        review = storage.get(Review, self.review_id)
        if review is not None:
            storage.delete(review)
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
        data = {'text': 'toto2'}
        response = requests.put(url=self.url, data=json.dumps(data))
        headers = response.headers
        json_data = response.json()

        self.assertTrue(self.place == storage.get(Place, self.place_id))
        self.assertEqual(response.status_code, 200, WRONG_STATUS_CODE_MSG)
        self.assertEqual(
            headers['Content-Type'], 'application/json', WRONG_TYPE_RETURN_MSG)
        storage.reload()
        review = storage.get(Review, self.review_id)
        self.assertEqual(review.text, 'toto2')
        self.assertIn('user_id', json_data, MISSING_USER_ID_ATTR_MSG)
        self.assertIn('place_id', json_data, MISSING_PLACE_ID_ATTR_MSG)
        self.assertIn('text', json_data, MISSING_TEXT_ATTR_MSG)
        self.assertIn('created_at', json_data, MISSING_CREATED_AT_ATTR_MSG)
        self.assertIn('updated_at', json_data, MISSING_UPDATED_AT_ATTR_MSG)
        self.assertIn('__class__', json_data, MISSING_CLASS_ATTR_MSG)
        self.assertEqual(json_data['user_id'], self.user_id)
        self.assertEqual(json_data['place_id'], self.place_id)
        self.assertEqual(json_data['text'], review.text)
        storage.delete(review)
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
