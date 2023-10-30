#!/usr/bin/python3
"""
Contains the TestStateDocs classes
"""

import pep8
import unittest


class TestamenDocs(unittest.TestCase):
    """Tests to check the documentation and style of State class"""

    def test_pep8_conformance_amen(self):
        """Test that models/amen.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['api/v1/views/users.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")
