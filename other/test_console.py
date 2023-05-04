#!/usr/bin/python3
"""
This is module test_console.
This module is a unittest for the console module.
it can be run with python -m unittest tests/test_console.py from
the parent directory
"""
import unittest
import sys
from unittest.mock import create_autospec
from io import StringIO
import os
sys.path.insert(0, os.path.join(os.path.split(__file__)[0], '..'))
import console


class TestConsole(unittest.TestCase):
    """
    This class is a unittest for the console module

    **Instance methods**
    """
    def setUp(self):
        """Redirects stdin and stdout"""
        self.mock_stdin = create_autospec(sys.stdin)
        self.mock_stdout = create_autospec(sys.stdout)

    def create(self):
        """Create instance"""
        return console.HBNBCommand(stdin=self.mock_stdin, stdout=self.mock_stdout)

    def _last_write(self):
        """return what was printed"""
        return self.mock_stdout.write.call_args[0][0]

    def test_help(self):
        """
        Tests the help command
        """
        cli = self.create()
        self.assertFalse(cli.onecmd("help"))
        self.assertFalse(self.mock_stdout.flush.called)
        # must redirect print to something, needs a return value
        self.assertEqual("""\nDocumented commands (type help <topic>):\n
                    ========================================
                        \nEOF  help  quit\n""",
                             self._last_write())

    def test_quit(self):
        cli = self.create()
        self.assertTrue(cli.onecmd("quit"))

    def test_EOF(self):
        cli = self.create()
        self.assertTrue(cli.onecmd("EOF"))

if __name__ == "__main__":
    unittest.main()
