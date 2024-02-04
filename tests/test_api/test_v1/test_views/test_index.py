#!/usr/bin/python3
"""
Test module for API index route
"""
import json
from os import getenv
import unittest
from unittest import mock
from api.v1.app import app


STORAGE_TYPE = getenv("HBNB_TYPE_STORAGE")

@unittest.skipIf(STORAGE_TYPE != 'db', "no database test")
class TestIndex(unittest.TestCase):
    """Test the index route for the API app"""
    def test_index_status(self):
        """Test the index HTTP response code"""
        testter = app.test_client()
        status_res = testter.get('/status')
        stats_res = testter.get('/stats')

        self.assertEqual(status_res.status_code, 200)
        self.assertEqual(stats_res.status_code, 200)

    def test_index_ContentType(self):
        """Test the response content type"""
        testter = app.test_client()
        status_res = testter.get('/status')
        stats_res = testter.get('/stats')

        self.assertEqual(status_res.content_type, "application/json")
        self.assertEqual(stats_res.content_type, "application/json")

    def test_status_content(self):
        """Test the content of the /status response"""
        message = {"status": "OK"}
        testter = app.test_client()
        res = testter.get('/status')
        self.assertDictEqual(json.loads(res.get_json()), message)

    @unittest.skipIf(STORAGE_TYPE == 'db', "no database test")
    def test_stats_content_db(self):
        """Test the content of the /stats response"""
        import MySQLdb

        message = {
            "amenities": "amenities",
            "cities": "cities",
            "places": "places",
            "reviews": "reviews",
            "states": "states",
            "users": "users"
            }
        HOST = getenv("HBNB_MYSQL_HOST")
        DB = getenv("HBNB_MYSQL_DB")
        USER = getenv("HBNB_MYSQL_USER")
        PASSWORD = getenv("HBNB_MYSQL_PWD")
        db_conn = MySQLdb.connect(
            host=HOST, database=DB,
            user=USER, password=PASSWORD)
        cur = db.conn.cursor()
        for table in message.values():
            cur.execute('SELECT count(*) FROM {};'.format(table))
            meassge[table] = int(cur.first())
        db_conn.commit()
        cur.close()
        db_conn.close()
        testter = app.test_client()
        res = testter.get('/stats')
        self.assertDictEqual(json.loads(res.to_json()), message)
