#!/usr/bin/python3
"""
Contains the TestIndexDocs
"""
import unittest


class TestV1ViewsIndex(unittest.TestCase):
    def test_imports(self):
        """Test on Import"""
        try:
            from api.v1.views import app_views
        except ImportError:
            self.fail("Failed to import necessary modules")

    def test_status_route(self):
        """Test on status"""
        from api.v1.views.index import app_views
        self.assertIsNotNone(app_views.url_prefix)
        self.assertTrue(any(rule.rule == '/status'
                            for rule in app_views.url_rules))
