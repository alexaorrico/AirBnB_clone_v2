#!/usr/bin/python3
"""
jut for test
"""

# test_example.py

import unittest


class TestExample(unittest.TestCase):

    def test_addition(self):
        result = 2 + 2
        self.assertEqual(result, 4, "Addition failed: 2 + 2 is not 4")


if __name__ == '__main__':
    unittest.main()
