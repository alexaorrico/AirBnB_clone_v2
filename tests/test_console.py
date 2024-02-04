#!/usr/bin/python3
"""
Contains the class TestConsoleDocs
"""

import console      
import inspect
import pep8
import unittest
import inspect
from console import HBNBCommand
HBNBCommand = console.HBNBCommand


class TestConsoleDocs(unittest.TestCase):
    """Class for testing documentation of the console"""
    def test_pep8_conformance_console(self):
        """Test that console.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['console.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_console(self):
        """Test that tests/test_console.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_console.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_console_module_docstring(self):
        """Test for the console.py module docstring"""
        self.assertIsNot(console.__doc__, None,
                         "console.py needs a docstring")
        self.assertTrue(len(console.__doc__) >= 1,
                        "console.py needs a docstring")

    def test_HBNBCommand_class_docstring(self):
        """Test for the HBNBCommand class docstring"""
        self.assertIsNot(HBNBCommand.__doc__, None,
                         "HBNBCommand class needs a docstring")
        self.assertTrue(len(HBNBCommand.__doc__) >= 1,
                        "HBNBCommand class needs a docstring")
import unittest
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand

class TestConsoleCommands(unittest.TestCase):
    """Class for testing console commands"""

    @patch('sys.stdout', new_callable=StringIO)
    def test_create(self, mock_stdout):
        """Test create command"""
        console = HBNBCommand()
        console.onecmd("create BaseModel")
        self.assertIn("Missing required attribute", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_show(self, mock_stdout):
        """Test show command"""
        console = HBNBCommand()
        console.onecmd("show BaseModel")
        self.assertIn("Missing required id", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_destroy(self, mock_stdout):
        """Test destroy command"""
        console = HBNBCommand()
        console.onecmd("destroy BaseModel")
        self.assertIn("Missing required id", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_all(self, mock_stdout):
        """Test all command"""
        console = HBNBCommand()
        console.onecmd("all")
        self.assertIn("BaseModel", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_update(self, mock_stdout):
        """Test update command"""
        console = HBNBCommand()
        console.onecmd("update BaseModel")
        self.assertIn("Missing required id", mock_stdout.getvalue())

if __name__ == '__main__':
    unittest.main()