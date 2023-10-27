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
    """Class for testing documentation of the console"""

    def test_pep8_conformance_console(self):
        """Test that console.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(["console.py"])
        self.assertEqual(
            result.total_errors, 0, "Found code style errors (and warnings)."
        )

    def test_pep8_conformance_test_console(self):
        """Test that tests/test_console.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(["tests/test_console.py"])
        self.assertEqual(
            result.total_errors, 0, "Found code style errors (and warnings)."
        )

    def test_console_module_docstring(self):
        """Test for the console.py module docstring"""
        msg = "console.py needs a docstring"
        self.assertIsNot(console.__doc__, None, msg)
        self.assertTrue(len(console.__doc__) >= 1, msg)

    def test_HBNBCommand_class_docstring(self):
        """Test for the HBNBCommand class docstring"""
        msg = "HBNBCommand class needs a docstring"
        self.assertIsNot(
            HBNBCommand.__doc__, None, msg
        )
        self.assertTrue(
            len(HBNBCommand.__doc__) >= 1, msg
        )
