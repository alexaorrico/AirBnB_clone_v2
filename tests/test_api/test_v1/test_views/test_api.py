#!/usr/bin/python3
''' Test for App '''
import unittest
import pep8
import json
import os
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

class TestApi(unittest.TestCase):
    ''' This will test the API '''

    @classmethod
    def setUpClass(cls):
        ''' Set up for test '''
        pass

    def tearDown(self):
        ''' At the end of the test, set up info will teardown '''
        pass

    def test_pep8_FileStorage(self):
        """Tests pep8 style"""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(['api/*.py'])
        self.assertEqual(p.total_errors, 0, "fix pep8")

if __name__ == "__main__":
    unittest.main()
