#!/usr/bin/python3
"""Test module for API cities route"""
import json
import MySQLdb
from os import getenv
import unittest
from unittest import mock
from api.v1.app import app, storage


STORAGE_TYPE = getenv("HBNB_TYPE_STORAGE")
HOST = getenv("HBNB_MYSQL_HOST")
DB = getenv("HBNB_MYSQL_DB")
USER = getenv("HBNB_MYSQL_USER")
PASSWORD = getenv("HBNB_MYSQL_PWD")


@unittest.skipIf(STORAGE_TYPE != 'db', "no db storage test")
class TestCities(unittest.TestCase):
    """Test the cities routes for the API"""
    def test_cities_GetStateCities_statusCode_contentType(self):
        """Test /states/<state_id>/cities route with get request"""
        db_conn = MySQLdb.connect(
            host=HOST, database=DB,
            user=USER, password=PASSWORD)
        cur = db_conn.cursor()
        cur.execute(
            """
            INSERT INTO states (id, name)
            VALUES ("8f165686-c98d-46d9-87d9-d6059adefd99", "Umdorman");
            """)
        cur.execute(
            """
            INSERT INTO cities (id, name, state_id)
            VALUES ("1da255c0-f023-4779-8134-2b1b40f87683", "Tharwa-18",
            "8f165686-c98d-46d9-87d9-d6059adefd99");
            """)
        cur.execute(
            """
            INSERT INTO cities (id, name, state_id)
            VALUES ("1da255c0-f023-4779-8134-2b1b40f876f8", "Tharwa-41",
            "8f165686-c98d-46d9-87d9-d6059adefd99");
            """)
        cur.execute(
            """
            INSERT INTO cities (id, name, state_id)
            VALUES ("1da255c0-f023-4779-8134-2b1b40f8763f", "Tharwa-21",
            "8f165686-c98d-46d9-87d9-d6059adefd99");
            """)
        db_conn.commit()
        cur.close()
        db_conn.close()

        testter = app.test_client()
        res = testter.get(
            '/api/v1/states/8f165686-c98d-46d9-87d9-d6059adefd99/cities'
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content_type, 'application/json')
        cities = json.loads(res.to_json())
        self.assertIsInstance(cities, list)        
        for city in cities:
            self.assertIsInstance(city, dict)
            self.assertEqual(city["state_id"],
                             "8f165686-c98d-46d9-87d9-d6059adefd99")
            self.assertEqual(city["__class__"], "City")

    def test_cities_GetState(self):
        """Test /cities/<city_id> route with get request"""
        # storage.__init__()
        # storage.reload()
        # storage.close()

        db_conn = MySQLdb.connect(
            host=HOST, database=DB,
            user=USER, password=PASSWORD)
        cur = db_conn.cursor()
        cur.execute(
            """
            INSERT INTO states (id, name)
            VALUES ("8f165686-c98d-46d9-87d9-d6059adefddd", "Bahri");
            """)
        cur.execute(
            """
            INSERT INTO cities (id, name, state_id)
            VALUES ("8f165686-ffff-46d9-87d9-d6059ade2d99", "Nabtah",
            "8f165686-c98d-46d9-87d9-d6059adefddd");
            """)
        db_conn.commit()
        cur.close()
        db_conn.close()

        testter = app.test_client()
        res = testter.get('/api/v1/cities/8f165686-ffff-46d9-87d9-d6059ade2d99')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content_type, 'application/json')

        city = json.loads(res.to_json())
        self.assertEqual(city["__class__"], "City")
        self.assertEqual(city["id"], "8f165686-fff-46d9-87d9-d6059ade2d99")
        self.assertEqual(city["name"], "Nabtah")
        self.assertEqual(city["state_id"], "8f165686-c98d-46d9-87d9-d6059adefddd")

    def test_cities_GetState_statusCode_404(self):
        """Test /cities/<city_id> route with get request
           Wrong instance id
        """
        testter = app.test_client()
        res = testter.get('/api/v1/cities/1234nonono')
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.content_type, 'application/json')

    def test_cities_DelCities(self):
        """Test /cities/<city_id> route with get request"""
        # storage.__init__()
        # storage.reload()
        # storage.close()

        db_conn = MySQLdb.connect(
            host=HOST, database=DB,
            user=USER, password=PASSWORD)
        cur = db_conn.cursor()
        cur.execute(
            """
            INSERT INTO states (id, name)
            VALUES ("8f165686-c98d-46d9-dffd-d6059ade2df9", "Soopa");
            """)
        cur.execute(
            """
            INSERT INTO cities (id, name, state_id)
            VALUES ("8f1fe686-ffff-46d9-87d9-d6059ade2dff", "Nabtah",
            "8f165686-c98d-46d9-dffd-d6059adefddd");
            """)
        db_conn.commit()
        cur.close()
        db_conn.close()
        testter = app.test_client()
        res = testter.delete('/api/v1/cities/8f1fe686-ffff-46d9-87d9-d6059ade2dff')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content_type, 'application/json')
        self.assertDictEqual(json.loads(res.to_json()), {})

    def test_cities_DelCities_statusCode_404(self):
        """Test /cities/<state_id> route with delete request
           Wrong instance id
        """
        testter = app.test_client()
        res = testter.delete('/api/v1/cities/1234nonono')
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.content_type, 'application/json')

    def test_cities_PostCity_statusCode(self):
        """Test /states/<state_id>/cities route with post request"""
        db_conn = MySQLdb.connect(
            host=HOST, database=DB,
            user=USER, password=PASSWORD)
        cur = db_conn.cursor()
        cur.execute(
            """
            INSERT INTO states (id, name)
            VALUES ("8f165686-c98d-46d9-2376-d6059ade0f23", "Jazeera");
            """)
        db_conn.commit()
        cur.close()
        db_conn.close()

        testter = app.test_client()
        res = testter.post(
            '/api/v1/states/8f165686-c98d-46d9-2376-d6059ade0f23/cities',
            json={'name': 'Madani'})
        city = json.loads(res.to_json())

        self.assertEqual(res.status_code, 201)
        self.assertEqual(city["__class__"], "City")
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(city["name"], "Madani")

    def test_cities_PostState_statusCode_400(self):
        """Test /states route with post request
           Not a JSON"""
        db_conn = MySQLdb.connect(
            host=HOST, database=DB,
            user=USER, password=PASSWORD)
        cur = db_conn.cursor()
        cur.execute(
            """
            INSERT INTO states (id, name)
            VALUES ("8f165686-cc0c-56df-2376-d6059ade0f23", "JazeeraS");
            """)
        db_conn.commit()
        cur.close()
        db_conn.close()

        testter = app.test_client()
        res = testter.post(
            '/api/v1/states/8f165686-cc0c-56df-2376-d6059ade0f23/cities',
            data={'name': 'Fariss \ Sudan'})
        state = json.loads(res.to_json())

        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(state, "Not a JSON")

    def test_cities_PostState_statusCode_400_missingName(self):
        """Test /states route with post request
            Missing name on the requests"""
        db_conn = MySQLdb.connect(
            host=HOST, database=DB,
            user=USER, password=PASSWORD)
        cur = db_conn.cursor()
        cur.execute(
            """
            INSERT INTO states (id, name)
            VALUES ("ff165686-cc0c-56df-b3df-d6059ade0f23", "JazeeraN");
            """)
        db_conn.commit()
        cur.close()
        db_conn.close()

        testter = app.test_client()
        res = testter.post(
            '/api/v1/states/ff165686-cc0c-56df-b3df-d6059ade0f23/cities',
            json={'name2': 'Khartoum'})
        state = json.loads(res.to_json())

        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(state, "Missing name")

    def test_cities_PutState(self):
        """Test /cities/<state_id> with put request"""
        db_conn = MySQLdb.connect(
            host=HOST, database=DB,
            user=USER, password=PASSWORD)
        cur = db_conn.cursor()
        cur.execute(
            """
            INSERT INTO states (id, name)
            VALUES ("df16568d-c98d-46d9-91f5-d6039ade0d0b", "PortSudan");
            """)
        cur.execute(
            """
            INSERT INTO cities (id, name, state_id)
            VALUES ("df160f8d-c98d-dcd1-91f5-d6039ade0d0b", "Kasala",
            "df16568d-c98d-46d9-91f5-d6039ade0d0b");
            """)
        db_conn.commit()
        cur.close()
        db_conn.close()

        testter = app.test_client()
        res = testter.put('/api/v1/cities/df16568d-c98d-46d9-91f5-d6039ade0d0b"',
                          json={'name': 'Sawakin',
                                'id': '8f165686-c98d-46d9-87d9-d6059ade2fff',
                                'state_id': 'df16c68d-c382-46d9-ed30-d6039ade0d01'})
        city = json.loads(res.to_json())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(city["__class__"], "City")
        self.assertEqual(city["name"], "Sawakin")
        self.assertTrue(city["id"] != "8f165686-c98d-46d9-87d9-d6059ade2fff")
        self.assertTrue(city["id"] == "8f165686-c98d-46d9-87d9-d6059ade2dff")
        self.assertTrue(city["state_id"] == "df16568d-c98d-46d9-91f5-d6039ade0d0b")
        self.assertTrue(city["state_id"] != "df16c68d-c382-46d9-ed30-d6039ade0d01")

    def test_cities_PutState_statusCode_404_WrongId(self):
        """Test /cities/<city_id> route with put request
           Wrong instance id
        """
        testter = app.test_client()
        res = testter.put('/api/v1/cities/1234nonono',
                          json={'name': 'NotLouisiana3',
                                'id': '8f165686-c98d-46d9-87d9-d6059ade2fff'})
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.content_type, 'application/json')

    def test_cities_PutState_statusCode_400_NotJSON(self):
        """Test /cities/<city_id> route with put request
           Wrong JSON format
        """
        res = testter.put('/api/v1/cities/df160f8d-c98d-dcd1-91f5-d6039ade0d0b',
                          data={'name': 'NotLouisiana3 \ yes',
                                'id': '8f165686-c98d-46d9-87d9-d6059ade2fff'})

        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(json.loads(res.to_json()), 'Not a JSON')

    def test_cities_GetCities_returnValue(self):
        """
        TODO: ADD TEST CASE FOR get('/api/v1/states/<state_id>/cities')
        RETURN VALUE
        """
        pass
