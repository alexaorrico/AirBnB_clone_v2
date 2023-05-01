#!/usr/bin/python3
"""
test console
"""
import unittest
from unittest.mock import patch
from io import StringIO
import pep8
import pep8 as pycodestyle
import os
import json
import console
import tests
import inspect
import models
from console import HBNBCommand
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage
Model = HBNBCommand
City = HBNBCommand
module_doc = HBNBCommand.__doc__
path1 = "console.py"
path2 = "tests/test_console.py"
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


class TestBaseModelDocs(unittest.TestCase):
    """Test to check behaviors"""

    @classmethod
    def setUpClass(self):
        """setting up tests"""
        self.base_funcs = inspect.getmembers(BaseModel, inspect.isfunction)

    def test_pep8(self):
        """Testing pep8"""
        for path in [path1,
                     path2]:
            with self.subTest(path=path):
                errors = pycodestyle.Checker(path).check_all()
                self.assertEqual(errors, 0)

    def test_module_docstring(self):
        """Test module docstring"""
        self.assertIsNot(module_doc, None,
                         "base_model.py needs a docstring")
        self.assertTrue(len(module_doc) > 1,
                        "base_model.py needs a docstring")

    def test_class_docstring(self):
        """Test classes doctring"""
        self.assertIsNot(BaseModel.__doc__, None,
                         "BaseModel class needs a docstring")
        self.assertTrue(len(BaseModel.__doc__) >= 1,
                        "BaseModel class needs a docstring")

    def test_func_docstrings(self):
        """test func dostrings"""
        for func in self.base_funcs:
            with self.subTest(function=func):
                self.assertIsNot(
                    func[1].__doc__,
                    None,
                    "{:s} method needs a docstring".format(func[0])
                )
                self.assertTrue(
                    len(func[1].__doc__) > 1,
                    "{:s} method needs a docstring".format(func[0])
                )


class ConsoleTest(unittest.TestCase):
    """testing console"""

    @classmethod
    def setUpClass(self):
        """setting class up"""
        self.console = HBNBCommand()

    def test_docstrings(self):
        """testing docstings"""
        self.assertIsNotNone(console.__doc__)
        self.assertIsNotNone(HBNBCommand.emptyline.__doc__)
        self.assertIsNotNone(HBNBCommand.do_quit.__doc__)
        self.assertIsNotNone(HBNBCommand.do_EOF.__doc__)
        self.assertIsNotNone(HBNBCommand.do_create.__doc__)
        self.assertIsNotNone(HBNBCommand.do_show.__doc__)
        self.assertIsNotNone(HBNBCommand.do_destroy.__doc__)
        self.assertIsNotNone(HBNBCommand.do_all.__doc__)
        self.assertIsNotNone(HBNBCommand.do_update.__doc__)
        self.assertIsNotNone(HBNBCommand.default.__doc__)

    def test_non_exist_command(self):
        """testing a command that doesn't exist like goku"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("goku")
            self.assertEqual('*** Unknown syntax: goku\n' or '',
                             f.getvalue())

    def test_empty_line(self):
        """testing empty input"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("\n")
            self.assertEqual('', f.getvalue())


@unittest.skipIf(type(models.storage) == DBStorage, "Testing DBStorage")
class CreateTest(unittest.TestCase):
    """testing command test in console"""

    @classmethod
    def setUpClass(self):
        """setting class up"""
        self.console = HBNBCommand()

    def test_create(self):
        """testing creat input"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create")
            self.assertEqual("** class name missing **\n",
                             f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create holbieees")
            self.assertEqual("** class doesn't exist **\n",
                             f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            HBNBCommand().onecmd("create User")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all User")
            self.assertEqual(
                            '[[User]', f.getvalue()[:7])
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
        self.assertRegex(f.getvalue(), '^[0-9a-f]{8}-[0-9a-f]{4}-[1-5]'
                                       '[0-9a-f]{3}-[89ab][0-9a-f]{3}-'
                                       '[0-9a-f]{12}$')
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create User")
        self.assertRegex(f.getvalue(), '^[0-9a-f]{8}-[0-9a-f]{4}-[1-5]'
                                       '[0-9a-f]{3}-[89ab][0-9a-f]{3}-'
                                       '[0-9a-f]{12}$')
