#!/usr/bin/python3
""" Module doc"""
import unittest
import console


class test_Console(unittest.TestCase):
    """doc doc"""

    def test_documentation(self):
        """doc doc"""
        self.assertIsNotNone(console.__doc__)
