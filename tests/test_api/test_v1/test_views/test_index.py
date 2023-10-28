#!usr/bin/python3
""" Test index view """
import unittest
import os
import pep8
from models import storage
import api.v1.app


class TestIndex(unittest.TestCase):
    """ Test the index view """

    def setUp(self):
        """ Setup for testing """
        api.v1.app.app.testing = True
        self.app = api.v1.app.app.test_client()

    def test_status(self):
        """ Test api/v1/views/status """
        rv = self.app.get('api/v1/status')
        assert b'status' in rv.data

    def test_stats(self):
        """ Test api/v1/stats """
        rv = self.app.get('api/v1/stats')
        assert b'amenities' in rv.data
        assert b'cities' in rv.data
        assert b'reviews' in rv.data
        assert b'states' in rv.data
        assert b'users' in rv.data
