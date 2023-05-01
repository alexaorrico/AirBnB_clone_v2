#!/usr/bin/python3
"""
Contains the TestStateDocs classes
"""

from datetime import datetime
import inspect
import models
import os
from models import state
from models.base_model import BaseModel
import pep8
import unittest
from api.v1 import app
from api.v1.views import states as test_state
from api.v1.views import amenities
from api.v1.views import cities
from api.v1.views import index
from api.v1.views import places_reviews
from api.v1.views import places_amenities
from api.v1.views import places
from api.v1.views import users
State = state.State


class TestStateDocs(unittest.TestCase):
    """Tests to check the documentation for all api files"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.state_f = inspect.getmembers(State, inspect.isfunction)

    def test_pep8_conformance_app(self):
        """Test that models/state.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['api/v1/app.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_states(self):
        """Test that models/state.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['api/v1/views/states.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_amenities(self):
        """Test that models/state.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['api/v1/views/amenities.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_cities(self):
        """Test that models/state.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['api/v1/views/cities.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_places_rev(self):
        """Test that models/state.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['api/v1/views/places_reviews.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_places(self):
        """Test that models/state.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['api/v1/views/places.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_users(self):
        """Test that models/state.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['api/v1/views/users.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_index(self):
        """Test that models/state.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['api/v1/views/index.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_pep8(self):
        """Test that tests/test_models/test_state.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_api/test_pep8.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_places_amenities(self):
        """Test that tests/test_models/test_state.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['api/v1/views/places_amenities.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

# file docstring

    def test_state_module_docstring_app(self):
        """Test for the state.py module docstring"""
        self.assertIsNot(app.__doc__, None,
                         "state.py needs a docstring")
        self.assertTrue(len(app.__doc__) >= 1,
                        "state.py needs a docstring")

    def test_state_class_docstring_state(self):
        """Test for the State class docstring"""
        self.assertIsNot(test_state.__doc__, None,
                         "State class needs a docstring")
        self.assertTrue(len(test_state.__doc__) >= 1,
                        "State class needs a docstring")

    def test_state_class_docstring_amenities(self):
        """Test for the State class docstring"""
        self.assertIsNot(amenities.__doc__, None,
                         "State class needs a docstring")
        self.assertTrue(len(amenities.__doc__) >= 1,
                        "State class needs a docstring")

    def test_state_class_docstring_cities(self):
        """Test for the State class docstring"""
        self.assertIsNot(cities.__doc__, None,
                         "State class needs a docstring")
        self.assertTrue(len(cities.__doc__) >= 1,
                        "State class needs a docstring")

    def test_state_class_docstring_index(self):
        """Test for the State class docstring"""
        self.assertIsNot(index.__doc__, None,
                         "State class needs a docstring")
        self.assertTrue(len(index.__doc__) >= 1,
                        "State class needs a docstring")

    def test_state_class_docstring_rev(self):
        """Test for the State class docstring"""
        self.assertIsNot(places_reviews.__doc__, None,
                         "State class needs a docstring")
        self.assertTrue(len(places_reviews.__doc__) >= 1,
                        "State class needs a docstring")

    def test_state_class_docstring_places(self):
        """Test for the State class docstring"""
        self.assertIsNot(places.__doc__, None,
                         "State class needs a docstring")
        self.assertTrue(len(places.__doc__) >= 1,
                        "State class needs a docstring")

    def test_state_class_docstring_users(self):
        """Test for the State class docstring"""
        self.assertIsNot(users.__doc__, None,
                         "State class needs a docstring")
        self.assertTrue(len(users.__doc__) >= 1,
                        "State class needs a docstring")

    def test_state_class_docstring_amenities_rev(self):
        """Test for the State class docstring"""
        self.assertIsNot(places_amenities.__doc__, None,
                         "State class needs a docstring")
        self.assertTrue(len(users.__doc__) >= 1,
                        "State class needs a docstring")

# dosctring tests

    def test_state_func_docstrings(self):
        """Test for the presence of docstrings in State methods"""
        for func in self.state_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))

    def test_state_func_docstrings_index(self):
        """Test for the presence of docstrings in State methods"""
        index_f = inspect.getmembers(index, inspect.isfunction)
        for func in index_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))

    def test_state_func_docstrings_user(self):
        """Test for the presence of docstrings in State methods"""
        index_f = inspect.getmembers(users, inspect.isfunction)
        for func in index_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))

    def test_state_func_docstrings_places(self):
        """Test for the presence of docstrings in State methods"""
        index_f = inspect.getmembers(places, inspect.isfunction)
        for func in index_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))

    def test_state_func_docstrings_states(self):
        """Test for the presence of docstrings in State methods"""
        index_f = inspect.getmembers(test_state, inspect.isfunction)
        for func in index_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))

    def test_state_func_docstrings_place_rev(self):
        """Test for the presence of docstrings in State methods"""
        index_f = inspect.getmembers(places_reviews, inspect.isfunction)
        for func in index_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))

    def test_state_func_docstrings_amenity_rev(self):
        """Test for the presence of docstrings in State methods"""
        index_f = inspect.getmembers(places_amenities, inspect.isfunction)
        for func in index_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))

    def test_state_func_docstrings_cities(self):
        """Test for the presence of docstrings in State methods"""
        index_f = inspect.getmembers(cities, inspect.isfunction)
        for func in index_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))

    def test_state_func_docstrings_amenities(self):
        """Test for the presence of docstrings in State methods"""
        index_f = inspect.getmembers(amenities, inspect.isfunction)
        for func in index_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))
