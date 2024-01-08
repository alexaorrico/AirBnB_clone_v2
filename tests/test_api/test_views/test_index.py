#!/usr/bin/python3
""""module tests the view indexes"""
import os
import unittest
from models import storage
import api.v1.app


class TestIndex(unittest.TestCase):
    """ Testing index view"""

    def setup(self):
        """sets up the testing"""
        api.v1.app.testing = True
        self.app = api.v1.app.app.test_client()

    def test_status(self):
        """"Testing the status of api/v1/views"""
        dat = self.app.get('api/v1/status')
        assert b'status' in dat.data

    def test_stats(self):
        """testing the stats in api/v1"""
        dat = self.app.get('api/v1/stats')
        assert b'states' in dat.data
        assert b'cities' in dat.data
        assert b'places' in dat.data
        assert b'amenities' in dat.data
        assert b'users' in dat.data
        assert b'reviews' in dat.data
