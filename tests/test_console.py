#!/usr/bin/python3
"""Test for console"""
import unittest

from console import HBNBCommand
from unittest.mock import patch
from io import StringIO
import models


class ConsoleTestCase(unittest.TestCase):
    """Test for console"""

    def setUp(self):
        self.console = HBNBCommand()
        self.stdout = StringIO()
        self.storage = models.storage
        self.cli = HBNBCommand()

    def tearDown(self):
        """ set down as in tear down """
        del self.stdout
        del self.storage
        self.cli = None

    def test_do_create_valid_class(self):
        """ all """
        with patch('models.storage.new') as new_mock, \
                patch('models.storage.save') as save_mock, \
                patch('sys.stdout', new=StringIO()) as f:
            self.cli.do_create("BaseModel")
            new_mock.assert_called_once()
            save_mock.assert_called_once()
            output = f.getvalue().strip()
            o = '^[0-9a-f]{8}(-[0-9a-f]{4}){3}-[0-9a-f]{12}$'
            self.assertRegex(output, o)

    def test_all(self):
        """test all"""
        with patch('sys.stdout', self.stdout):
            self.console.onecmd('create State name="California"')
        with patch('sys.stdout', self.stdout):
            self.console.onecmd('all State')
        output = self.stdout.getvalue()[:-1]
        self.assertIn("State", output)
        self.assertIn("California", output)

    @unittest.skip("not right now")
    def test_update(self):
        with patch('sys.stdout', self.stdout):
            self.console.onecmd('create State name="California"')
        state_id = self.stdout.getvalue()[:-1]
        with patch('sys.stdout', self.stdout):
            self.console.onecmd(
                'update State {} name="New California"'.format(state_id))
        with patch('sys.stdout', self.stdout):
            self.console.onecmd('show State {}'.format(state_id))
        output = self.stdout.getvalue()[:-1]
        self.assertIn("California", output)

    def test_destroy(self):
        """test destroy"""
        with patch('sys.stdout', self.stdout):
            self.console.onecmd('create State name="California"')
        state_id = self.stdout.getvalue()[:-1]
        with patch('sys.stdout', self.stdout):
            self.console.onecmd('destroy State {}'.format(state_id))
        # with patch('sys.stdout', self.stdout):
        #     self.console.onecmd('show State {}'.format(state_id))
        # self.assertEqual("** no instance found **\n",
        #                  self.stdout.getvalue())

    def test_show(self):
        """test show"""
        with patch('sys.stdout', self.stdout):
            self.console.onecmd('create State name="California"')
        state_id = self.stdout.getvalue()[:-1]
        with patch('sys.stdout', self.stdout):
            self.console.onecmd('show State {}'.format(state_id))
        output = self.stdout.getvalue()[:-1]
        self.assertIn("California", output)

    def test_do_create_no_args(self):
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.do_create("")
            self.assertEqual(f.getvalue().strip(), "** class name missing **")

    def test_do_create_invalid_class(self):
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.do_create("MyClass")
            self.assertEqual(f.getvalue().strip(), "** class doesn't exist **")
