#!/usr/bin/python3
"""Test file for app.py"""
import os
from api.v1.app import app
import unittest
import tempfile


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        """setUp method for Flask test class"""
        self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        flaskr.app.testing = True
        self.app = flaskr.app.test_client()
        with flaskr.app.app_context():
            flaskr.init_db()

    def tearDown(self):
        """tearDown method for flask unittest"""
        os.close(self.db_fd)
        os.unlink(flaskr.app.config["DATABASE"])

    def test_empty_db(self):
        """Testing for no entries in empty databases"""
        rv = self.app.get('/')
        self.assertEqual("No entries here so far", rv.data)

if __name__ == "__main__":
    print("RAN TEST")
    unittest.main()
