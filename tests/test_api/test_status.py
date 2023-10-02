#!/usr/bin/python3
"""test to determine if the api service returns the right
working status
"""

from models import storage
import unittest
from api.v1.app import app

class TestServiceStatus(unittest.TestCase):
    """test the status to see if the server is responsive
    """
    def test_on_status(self):
        """test ON status
        """
        
