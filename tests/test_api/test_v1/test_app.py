#!/usr/bin/python3
"""
Contains the TestappDocs classes
"""

from datetime import datetime
import inspect
import models
from models import state
from models.base_model import BaseModel
import pep8
import unittest


class TestappDocs(unittest.TestCase):
    """Tests to check the documentation and style of app class"""

    def test_pep8_conformance_app(self):
        """Test that models/app.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['api/v1/app.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")
