#!/usr/bin/python3
"""
Contains the TestAmenityDocs classes
"""

import unittest
from api.v1.app import app
import flask


class TestApiAppV1(unittest.TestCase):
    '''testing api app version 1'''
    def test_app(self):
        '''test test'''
        with app.test_request_context('/states'):
            assert flask.request.path == '/states'
