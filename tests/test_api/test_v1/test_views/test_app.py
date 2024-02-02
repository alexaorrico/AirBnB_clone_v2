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

    def status_ok(self):
        """ Check for status"""
        with app.test_client() as c:
            rv = c.get("...")
            json_data = rv.get_json()
            self.assertDictEqual(
                    json_data,
                    {"status": "OK"}
                    )
