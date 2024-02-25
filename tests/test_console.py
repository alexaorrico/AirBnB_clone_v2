#!/usr/bin/python3
"""
Contains the class TestConsoleDocs
"""

import console
import inspect
import pep8
import unittest

HBNBCommand = console.HBNBCommand


class TestConsoleDocs(unittest.TestCase):
    """Tests to check the documentation and style of console.py"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.console_funcs = inspect.getmembers(HBNBCommand, inspect.isfunction)

    def test_pep8_conformance_console(self):
        """Test that console.py conforms to PEP8."""
        pep8style = pep8.StyleGuide(quiet=True)
        result = pep8style.check_files(["console.py"])
        self.assertEqual(
            result.total_errors, 0, "Found code style errors (and warnings)."
        )

    def test_pep8_conformance_test_console(self):
        """Test that test_console.py conforms to PEP8."""
        pep8style = pep8.StyleGuide(quiet=True)
        result = pep8style.check_files(["tests/test_console.py"])
        self.assertEqual(
            result.total_errors, 0, "Found code style errors (and warnings)."
        )

    def test_module_docstring(self):
        """Test for the module docstring"""
        self.assertTrue(len(console.__doc__) > 0)

    def test_class_docstring(self):
        """Test for the class docstring"""
        self.assertTrue(len(HBNBCommand.__doc__) > 0)

    def test_func_docstrings(self):
        """Test for the presence of docstrings in HBNBCommand methods"""
        for func in self.console_funcs:
            self.assertTrue(len(func[1].__doc__) > 0)
