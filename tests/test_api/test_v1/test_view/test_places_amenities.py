#!/usr/bin/python3
"""
Contains the TestStateDocs classes
"""

from datetime import datetime
import inspect
import models
from models import state
from models.base_model import BaseModel
import pep8
import unittest


class TestplamDocs(unittest.TestCase):
    """Tests to check the documentation and style of plam class"""

    def test_pep8_conformance_plam(self):
        """Test that models/state.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['api/v1/views/users.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")
