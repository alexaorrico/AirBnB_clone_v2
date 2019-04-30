#!/usr/bin/python3
"""Test file for app.py"""
import os
from api.v1 import app
import unittest
import tempfile
from models import storage
from flask_mysqldb import MySQL


class AppTestCase(unittest.TestCase):

    def setUp(self):
        """setUp method for Flask test class"""
        app.app.config['MYSQL_HOST'] = 'localhost'
        app.app.config['MYSQL_USER'] = 'hbnb_test'
        app.app.config['MYSQL_PASSWORD'] = 'hbnb_test_pwd'
        app.app.config['MYSQL_DB'] = 'hbnb_test_db'
        self.db_fd, app.app.config['hbnb_test_db'] = tempfile.mkstemp()
        app.app.testing = True
        self.app = app.app.test_client()
        mysql = MySQL(app.app)
        with app.app.app_context():
            cur = mysql.connection.cursor()

    def tearDown(self):
        """tearDown method for flask unittest"""
        os.close(self.db_fd)
        os.unlink(app.app.config["hbnb_test_db"])

    def test_empty_db(self):
        """Testing for no entries in empty databases"""
        rv = self.app.get('/')
        print(rv.__dict__)
        print(dir(rv))
        self.assertEqual("No entries here so far", rv.data.decode('utf-8'))

if __name__ == "__main__":
    unittest.main()
