#!/usr/bin/python3
"""
Unit Test for Review Class
"""
import unittest
from datetime import datetime
import models
import json
import os

Review = models.review.Review
BaseModel = models.base_model.BaseModel
storage_type = os.environ.get('HBNB_TYPE_STORAGE')


class TestReviewDocs(unittest.TestCase):
    """Class for testing BaseModel docs"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('..... Testing Documentation .....')
        print('.......   Review  Class   .......')
        print('.................................\n\n')

    def test_doc_file(self):
        """... documentation for the file"""
        expected = '\nReview Class from Models Module\n'
        actual = models.review.__doc__
        self.assertEqual(expected, actual)

    def test_doc_class(self):
        """... documentation for the class"""
        expected = 'Review class handles all application reviews'
        actual = Review.__doc__
        self.assertEqual(expected, actual)


class TestReviewInstances(unittest.TestCase):
    """testing for class instances"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('....... Testing Functions .......')
        print('........  Review  Class  ........')
        print('.................................\n\n')

    def setUp(self):
        """initializes new review for testing"""
        self.review = Review()

    def test_instantiation(self):
        """... checks if Review is properly instantiated"""
        self.assertIsInstance(self.review, Review)

    @unittest.skipIf(storage_type == 'db', 'skip if environ is db')
    def test_to_string(self):
        """... checks if BaseModel is properly casted to string"""
        my_str = str(self.review)
        my_list = ['Review', 'id', 'created_at']
        actual = 0
        for sub_str in my_list:
            if sub_str in my_str:
                actual += 1
        self.assertTrue(3 == actual)

    @unittest.skipIf(storage_type == 'db', 'skip if environ is db')
    def test_instantiation_no_updated(self):
        """... should not have updated attribute"""
        my_str = str(self.review)
        actual = 0
        if 'updated_at' in my_str:
            actual += 1
        self.assertTrue(0 == actual)

    @unittest.skipIf(storage_type == 'db', 'skip if environ is db')
    def test_updated_at(self):
        """... save function should add updated_at attribute"""
        self.review.save()
        actual = type(self.review.updated_at)
        expected = type(datetime.now())
        self.assertEqual(expected, actual)

    @unittest.skipIf(storage_type == 'db', 'skip if environ is db')
    def test_to_json(self):
        """... to_json should return serializable dict object"""
        self.review_json = self.review.to_json()
        actual = 1
        try:
            serialized = json.dumps(self.review_json)
        except:
            actual = 0
        self.assertTrue(1 == actual)

    @unittest.skipIf(storage_type == 'db', 'skip if environ is db')
    def test_json_class(self):
        """... to_json should include class key with value Review"""
        self.review_json = self.review.to_json()
        actual = None
        if self.review_json['__class__']:
            actual = self.review_json['__class__']
        expected = 'Review'
        self.assertEqual(expected, actual)

    def test_review_attribute(self):
        """... add review attribute"""
        self.review.text = "This place smells"
        if hasattr(self.review, 'text'):
            actual = self.review.text
        else:
            acual = ''
        expected = "This place smells"
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main
