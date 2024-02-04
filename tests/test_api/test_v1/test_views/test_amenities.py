#!/usr/bin/python3
"""Test module for API amenities route"""
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
class TestAmenities(unittest.TestCase):
    """Test the amenities routes for the API"""
    def test_amenities(self):
        """Test /amenities route with get request"""
        db_conn = MySQLdb.connect(
            host=HOST, database=DB,
            user=USER, password=PASSWORD)
        cur = db.conn.cursor()
        cur.execute(
            """
            INSERT INTO amenities (id, name)
            VALUES ("1da255c0-f023-4779-28f8-2b1b40f8763f", "WIFI");
            """)
        cur.execute(
            """
            INSERT INTO amenities (id, name)
            VALUES ("1da255c0-f023-4779-0e5d-2b1b40f8763f", "PETS ALLOWED");
            """)
        cur.execute(
            """
            INSERT INTO amenities (id, name)
            VALUES ("1da255c0-f023-4779-5fef-2b1b40f8763f", "5G WIFI");
            """)
        db_conn.commit()
        cur.close()
        db_conn.close()

        testter = app.test_client()
        res = testter.get('/api/v1/amenities')

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content_type, 'application/json')
        amenities = json.loads(res.to_json())
        self.assertIsInstance(amenities, list)        
        for amenity in amenities:
            self.assertIsInstance(amenity, dict)
            self.assertEqual(city["__class__"], "Amenity")

    def test_amenity_by_id(self):
        """Test /amenities/<amenity_id> route with get request"""
        # storage.__init__()
        # storage.reload()
        # storage.close()

        db_conn = MySQLdb.connect(
            host=HOST, database=DB,
            user=USER, password=PASSWORD)
        cur = db.conn.cursor()
        cur.execute(
            """
            INSERT INTO amenities (id, name)
            VALUES ("1cfd55cf-f023-4779-5fef-2b1b40f8763f", "MALL");
            """)
        db_conn.commit()
        cur.close()
        db_conn.close()

        testter = app.test_client()
        res = testter.get('/api/v1/amenities/1cfd55cf-f023-4779-5fef-2b1b40f8763f')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content_type, 'application/json')

        amenity = json.loads(res.to_json())
        self.assertEqual(amenity["__class__"], "City")
        self.assertEqual(amenity["id"], "1cfd55cf-f023-4779-5fef-2b1b40f8763f")
        self.assertEqual(amenity["name"], "MALL")

    def test_amenities_404(self):
        """Test /amenities/<amenity_id> route with get request
           Wrong instance id
        """
        testter = app.test_client()
        res = testter.get('/api/v1/amenities/1234nonono')
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.content_type, 'application/json')

    def test_amenities_DelAmenity(self):
        """Test /amenities/<amenity_id> route with delete request"""
        # storage.__init__()
        # storage.reload()
        # storage.close()

        testter = app.test_client()
        res = testter.delete('/api/v1/amenities/1cfd55cf-f023-4779-5fef-2b1b40f8763f')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content_type, 'application/json')
        self.assertDictEqual(json.loads(res.to_json()), {})

        db_conn = MySQLdb.connect(
            host=HOST, database=DB,
            user=USER, password=PASSWORD)
        cur = db.conn.cursor()
        cur.execute(
            """
            SELECT * FROM amenities WHERE id=1cfd55cf-f023-4779-5fef-2b1b40f8763f;
            """)
        amenity = cur.fetchone()
        db_conn.commit()
        cur.close()
        db_conn.close()

        self.assertTrue(amenity is None)


    def test_amenities_DelAmenities_statusCode_404(self):
        """Test /amenities/<state_id> route with delete request
           Wrong instance id
        """
        testter = app.test_client()
        res = testter.delete('/api/v1/amenities/1234nonono')
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.content_type, 'application/json')

    def test_amenities_PostCity_statusCode(self):
        """Test /states/<state_id>/amenities route with post request"""
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
            '/api/v1/states/8f165686-c98d-46d9-2376-d6059ade0f23/amenities',
            json={'name': 'Madani'})
        city = json.loads(res.to_json())

        self.assertEqual(res.status_code, 201)
        self.assertEqual(city["__class__"], "City")
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(city["name"], "Madani")

    def test_amenities_PostState_statusCode_400(self):
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
            '/api/v1/states/8f165686-cc0c-56df-2376-d6059ade0f23/amenities',
            data={'name': 'Fariss \ Sudan'})
        state = json.loads(res.to_json())

        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(state, "Not a JSON")

    def test_amenities_PostState_statusCode_400_missingName(self):
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
            '/api/v1/states/ff165686-cc0c-56df-b3df-d6059ade0f23/amenities',
            json={'name2': 'Khartoum'})
        state = json.loads(res.to_json())

        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(state, "Missing name")

    def test_amenities_PutState(self):
        """Test /amenities/<state_id> with put request"""
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
            INSERT INTO amenities (id, name, state_id)
            VALUES ("df160f8d-c98d-dcd1-91f5-d6039ade0d0b", "Kasala",
            "df16568d-c98d-46d9-91f5-d6039ade0d0b");
            """)
        db_conn.commit()
        cur.close()
        db_conn.close()

        testter = app.test_client()
        res = testter.put('/api/v1/amenities/df16568d-c98d-46d9-91f5-d6039ade0d0b"',
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

    def test_amenities_PutState_statusCode_404_WrongId(self):
        """Test /amenities/<city_id> route with put request
           Wrong instance id
        """
        testter = app.test_client()
        res = testter.put('/api/v1/amenities/1234nonono',
                          json={'name': 'NotLouisiana3',
                                'id': '8f165686-c98d-46d9-87d9-d6059ade2fff'})
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.content_type, 'application/json')

    def test_amenities_PutState_statusCode_400_NotJSON(self):
        """Test /amenities/<city_id> route with put request
           Wrong JSON format
        """
        res = testter.put('/api/v1/amenities/df160f8d-c98d-dcd1-91f5-d6039ade0d0b',
                          data={'name': 'NotLouisiana3 \ yes',
                                'id': '8f165686-c98d-46d9-87d9-d6059ade2fff'})

        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(json.loads(res.to_json()), 'Not a JSON')

    def test_amenities_GetAmenities_returnValue(self):
        """
        TODO: ADD TEST CASE FOR get('/api/v1/amenities')
        RETURN VALUE
        """
        pass
