#!/usr/bin/python3
"""
Contains the TestAppDoc

"""

import unittest


class TestV1App(unittest.TestCase):
    def test_imports(self):
        """Test the imports of the necessary files"""
        try:
            from api.models import storage
            from api.v1.views import app_views
            from flask import Flask
        except ImportError:
            self.fail("Failed to import necessary modules")

    def test_blueprint_registered(self):
        """Test the Blueprint"""
        from api.v1.app import app
        self.assertIsNotNone(app.blueprints.get('app_views'))

    def test_teardown_appcontext(self):
        """Test the app"""
        from api.v1.app import app
        teardown_funcs = app.teardown_appcontext_functions
        self.assertTrue(any(func[0].__name__ == 'close'
                            for func in teardown_funcs))
