#!/usr/bin/python3
"""Test module for API state route"""
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


@unittest.skipIf(STORAGE.TYPE != 'db', "no db storage test")
class TestStates(unittest.TestCase):
    """Test the states routes for the API"""
    def test_states_GetAllStates_statusCode_contentType(self):
        """Test /states route with get request"""
        testter = app.test_client()
        res = tesster.get('/states')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content_type, 'application/json')

    def test_states_GetState(self):
        """Test /states/<state_id> route with get request"""
        # storage.__init__()
        # storage.reload()
        # storage.close()

        db_conn = MySQLdb.connect(
            host=HOST, database=DB,
            user=USER, password=PASSWORD)
        cur = db.conn.cursor()
        cur.execute(
            """
            INSERT INTO states (id, name)
            VALUES ("8f165686-c98d-46d9-87d9-d6059ade2d99", "Louisiana");
            """)
        db_conn.close()

        testter = app.test_client()
        res = tesster.get('/states/8f165686-c98d-46d9-87d9-d6059ade2d99')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content_type, 'application/json')

        state = json.loads(res.to_json())
        self.assertEqual(state["id"], "8f165686-c98d-46d9-87d9-d6059ade2d99")
        self.assertEqual(state["name"], "Louisiana")

    def test_states_GetState_statusCode_404(self):
        """Test /states/<state_id> route with get request
           Wrong instance id
        """
        testter = app.test_client()
        res = tesster.get('/states/1234nonono')
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.content_type, 'application/json')

    def test_states_DelStates(self):
        """Test /states/<state_id> route with get request"""
        # storage.__init__()
        # storage.reload()
        # storage.close()

        db_conn = MySQLdb.connect(
            host=HOST, database=DB,
            user=USER, password=PASSWORD)
        cur = db.conn.cursor()
        cur.execute(
            """
            INSERT INTO states (id, name)
            VALUES ("8f165686-c98d-46d9-87d9-d6059ade2df9", "Louisiana2");
            """)
        db_conn.close()
        testter = app.test_client()
        res = tesster.delete('/states/8f165686-c98d-46d9-87d9-d6059ade2df9')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content_type, 'application/json')
        self.assertDictEqual(json.loads(res.to_json()), {})

    def test_states_DelStates_statusCode_404(self):
        """Test /states/<state_id> route with delete request
           Wrong instance id
        """
        testter = app.test_client()
        res = tesster.delete('/states/1234nonono')
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.content_type, 'application/json')

    def test_states_PostState_statusCode(self):
        """Test /states route with post request"""
        testter = app.test_client()
        res = testter.post('/states', json={'name': 'Khartoum'})
        state = json.loads(res.to_json())

        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(state["name"], "Khartoum")

    def test_states_PostState_statusCode_400(self):
        """Test /states route with post request
           Not a JSON"""
        testter = app.test_client()
        res = testter.post('/states', data={'name': 'Khartoum \ Sudan'})
        state = json.loads(res.to_json())

        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(state, "Not a JSON")

    def test_states_PostState_statusCode_400_missingName(self):
        """Test /states route with post request
            Missing name on the requests"""
        testter = app.test_client()
        res = testter.post('/states', json={'name2': 'Khartoum'})
        state = json.loads(res.to_json())

        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(state, "Missing name")

    def test_states_PutState(self):
        """Test /states/<state_id> with put request"""
        db_conn = MySQLdb.connect(
            host=HOST, database=DB,
            user=USER, password=PASSWORD)
        cur = db.conn.cursor()
        cur.execute(
            """
            INSERT INTO states (id, name)
            VALUES ("8f165686-c98d-46d9-87d9-d6059ade2dff", "Louisiana3");
            """)
        db_conn.close()

        testter = app.test_client()
        res = testter.put('/states/8f165686-c98d-46d9-87d9-d6059ade2dff',
                          json={'name': 'NotLouisiana3',
                                'id': '8f165686-c98d-46d9-87d9-d6059ade2fff'})
        state = json.loads(res.to_json())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(state["name"], "NotLouisiana3")
        self.assertTrue(state["id"] != "8f165686-c98d-46d9-87d9-d6059ade2fff")
        self.assertTrue(state["id"] == "8f165686-c98d-46d9-87d9-d6059ade2dff")

    def test_states_PutState_statusCode_404_WrongId(self):
        """Test /states/<state_id> route with put request
           Wrong instance id
        """
        testter = app.test_client()
        res = tesster.put('/states/1234nonono',
                          json={'name': 'NotLouisiana3',
                                'id': '8f165686-c98d-46d9-87d9-d6059ade2fff'})
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.content_type, 'application/json')

    def test_states_PutState_statusCode_400_NotJSON(self):
        """Test /states/<state_id> route with put request
           Wrong JSON format
        """
        res = testter.put('/states/8f165686-c98d-46d9-87d9-d6059ade2dff',
                          data={'name': 'NotLouisiana3 \ yes',
                                'id': '8f165686-c98d-46d9-87d9-d6059ade2fff'})

        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(json.loads(res.to_json()), 'Not a JSON')
