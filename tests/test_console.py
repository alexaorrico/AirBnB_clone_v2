"""
Test air bnb console
"""

import os
import unittest
from io import StringIO
from unittest.mock import patch

import pep8

from console import HBNBCommand
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.engine.file_storage import FileStorage
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class TestConsole(unittest.TestCase):
    """Test console"""

    def test_pep8_console(self):
        """Test pep8 style"""
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(["console.py"])
        self.assertEqual(result.total_errors, 0, "fix pep8")

    def test_docstrings_in_console(self):
        """Test docstrings"""
        self.assertIsNotNone(HBNBCommand.__doc__)
        self.assertIsNotNone(HBNBCommand.do_quit.__doc__)
        self.assertIsNotNone(HBNBCommand.do_EOF.__doc__)
        self.assertIsNotNone(HBNBCommand.emptyline.__doc__)
        self.assertIsNotNone(HBNBCommand.do_create.__doc__)
        self.assertIsNotNone(HBNBCommand.do_show.__doc__)
        self.assertIsNotNone(HBNBCommand.do_destroy.__doc__)
        self.assertIsNotNone(HBNBCommand.do_all.__doc__)
        self.assertIsNotNone(HBNBCommand.do_update.__doc__)
        self.assertIsNotNone(HBNBCommand.do_count.__doc__)

    def test_create(self):
        """Test create"""
        with self.subTest("Test create State"):
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd("create State name=\"California\"")
                state_id = f.getvalue()
            self.assertTrue(len(state_id) > 0)
