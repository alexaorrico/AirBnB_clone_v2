#!/usr/bin/python3
"""
Contains the TestReviewDocs classes
"""

from datetime import datetime
import inspect
import models
from models import review
from models.base_model import BaseModel
import pep8
import unittest

Review = review.Review


class TestReviewDocs(unittest.TestCase):
    """Tests to check the documentation and style of Review class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.review_f = inspect.getmembers(Review, inspect.isfunction)

    def test_pep8_conformance_review(self):
        """Test that models/review.py conforms to PEP8."""
        pep8style = pep8.StyleGuide(quiet=True)
        result = pep8style.check_files(["models/review.py"])
        self.assertEqual(
            result.total_errors, 0, "Found code style errors (and warnings)."
        )

    def test_pep8_conformance_test_review(self):
        """Test that tests/test_models/test_review.py conforms to PEP8."""
        pep8style = pep8.StyleGuide(quiet=True)
        result = pep8style.check_files(["tests/test_models/test_review.py"])
        self.assertEqual(
            result.total_errors, 0, "Found code style errors (and warnings)."
        )

    def test_review_module_docstring(self):
        """Test for the review.py module docstring"""
        self.assertTrue(len(review.__doc__) > 0)

    def test_review_class_docstring(self):
        """Test for the Review class docstring"""
        self.assertTrue(len(Review.__doc__) > 0)

    def test_review_func_docstrings(self):
        """Test for the presence of docstrings in Review methods"""
        for func in self.review_f:
            self.assertTrue(len(func[1].__doc__) > 0)


class TestReview(unittest.TestCase):
    """Test the Review class"""

    def test_is_subclass(self):
        """Test that Review is a subclass of BaseModel"""
        review = Review()
        self.assertIsInstance(review, BaseModel)
        self.assertTrue(hasattr(review, "id"))
        self.assertTrue(hasattr(review, "created_at"))
        self.assertTrue(hasattr(review, "updated_at"))

    def test_place_id_attr(self):
        """Test that Review has place_id attribute."""
        review = Review()
        self.assertTrue(hasattr(review, "place_id"))
        if models.storage_t == "db":
            self.assertEqual(review.place_id, None)

    def test_user_id_attr(self):
        """Test that Review has user_id attribute."""
        review = Review()
        self.assertTrue(hasattr(review, "user_id"))
        if models.storage_t == "db":
            self.assertEqual(review.user_id, None)

    def test_text_attr(self):
        """Test that Review has text attribute."""
        review = Review()
        self.assertTrue(hasattr(review, "text"))
        if models.storage_t == "db":
            self.assertEqual(review.text, None)
