#!/usr/bin/python3
""" Functions to test whethher json givin response"""
import unittest
from api.v1.app import app


class TestStatus(unittest.TestCase):
    """ This class tests the status behaviour of
    the api"""
    def setUp(self):
        """ Set up method"""
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self):
        """Tear down context """
        self.ctx.pop()

    def test_status_ok(self):
        """ Check for status"""
        with app.test_client() as c:
            rv = c.get("/api/v1/status")
            json_data = rv.get_json()
            self.assertDictEqual(
                    json_data,
                    {"status": "OK"}
                    )

    def test_response_code(self):
        """ Test for the response code"""
        with app.test_client() as c:
            rv = c.get("/api/v1/status")
            self.assertEqual(rv.status_code, 200)


class TestError404(unittest.TestCase):
    """ This class tests for error404"""
    def test_response_code(self):
        """ Test for the response code"""
        with app.test_client() as c:
            rv = c.get("/api/v1/doesnotexist")
            self.assertEqual(rv.status_code, 404)

    def test_error_404(self):
        """ Test the error object itself"""
        with app.test_client() as c:
            rv = c.get("/api/v1/doesnotexist")
            json_data = rv.get_json()
            self.assertDictEqual(
                    json_data,
                    {"error": "Not found"}
                    )
