#!/usr/bin/python3
"""
Contains the class TestConsoleDocs and TestConsole
"""

import re
import console
import inspect
import pep8
import unittest
from unittest.mock import patch
from io import StringIO
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


class TestConsole(unittest.TestCase):
    """Class for testing the functionality of the console"""
    @patch('sys.stdout', new_callable=StringIO)
    def test_help_command(self, mock_stdout):
        """Test the help command"""
        cmd = HBNBCommand()
        cmd.onecmd("help")
        output = mock_stdout.getvalue()
        self.assertIn("Documented commands (type help <topic>):", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_create_command(self, mock_stdout):
        """Test the create command"""
        cmd = HBNBCommand()
        cmd.onecmd("create BaseModel")
        output = mock_stdout.getvalue().strip()
        # Check if output is a valid UUID
        uuid_regex = re.compile(
            r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$',
            re.I
        )
        self.assertTrue(uuid_regex.match(output), "Output is not a valid UUID")

    @patch('sys.stdout', new_callable=StringIO)
    def test_show_command(self, mock_stdout):
        """Test the show command"""
        cmd = HBNBCommand()
        cmd.onecmd('create BaseModel')
        model_id = mock_stdout.getvalue().strip()
        mock_stdout.truncate(0)
        mock_stdout.seek(0)
        cmd.onecmd('show BaseModel {}'.format(model_id))
        output = mock_stdout.getvalue()
        self.assertIn(model_id, output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_destroy_command(self, mock_stdout):
        """Test the destroy command"""
        cmd = HBNBCommand()
        cmd.onecmd('create BaseModel')
        model_id = mock_stdout.getvalue().strip()
        mock_stdout.truncate(0)
        mock_stdout.seek(0)
        cmd.onecmd('destroy BaseModel {}'.format(model_id))
        mock_stdout.truncate(0)
        mock_stdout.seek(0)
        cmd.onecmd('show BaseModel {}'.format(model_id))
        output = mock_stdout.getvalue()
        self.assertIn("no instance found", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_all_command(self, mock_stdout):
        """Test the all command"""
        cmd = HBNBCommand()
        cmd.onecmd('create BaseModel')
        model_id = mock_stdout.getvalue().strip()
        mock_stdout.truncate(0)
        mock_stdout.seek(0)
        cmd.onecmd('all BaseModel')
        output = mock_stdout.getvalue()
        self.assertIn(model_id, output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_update_command(self, mock_stdout):
        """Test the update command"""
        cmd = HBNBCommand()
        cmd.onecmd('create BaseModel')
        model_id = mock_stdout.getvalue().strip()
        mock_stdout.truncate(0)
        mock_stdout.seek(0)
        cmd.onecmd('update BaseModel {} name "Test"'.format(model_id))
        mock_stdout.truncate(0)
        mock_stdout.seek(0)
        cmd.onecmd('show BaseModel {}'.format(model_id))
        output = mock_stdout.getvalue()
        self.assertIn("Test", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_invalid_command(self, mock_stdout):
        """Test an invalid command"""
        cmd = HBNBCommand()
        cmd.onecmd("foobar")
        output = mock_stdout.getvalue()
        self.assertIn("*** Unknown syntax: foobar", output)
