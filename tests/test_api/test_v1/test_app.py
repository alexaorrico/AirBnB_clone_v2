from unittest import TestCase
from api.v1.app import app
from models import storage
import unittest


class TestIntegrations(TestCase):
    def setUp(self):
        """set up app for testing"""
        self.app = app.test_client()

    def tearDown(self):
        """ remove self.app """
        self.app = None


if __name__ == '__main__':
    unittest.main()
