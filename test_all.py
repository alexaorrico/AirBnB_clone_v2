import unittest

# Define your test class
class MyTestCase(unittest.TestCase):
    def test_addition(self):
        result = 2 + 2
        self.assertEqual(result, 4)  # Assertion to check if the result is 4

    def test_subtraction(self):
        result = 5 - 3
        self.assertEqual(result, 2)  # Assertion to check if the result is 2

# Run the tests
if __name__ == '__main__':
    unittest.main()
