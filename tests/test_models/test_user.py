import unittest
from datetime import datetime
from models import *


class Test_UserModel(unittest.TestCase):
    """
    Test the user model class
    """

    def test_no_arguments(self):
        """test initialization without arguments"""
        model = User()
        self.assertTrue(hasattr(model, "id"))
        self.assertTrue(hasattr(model, "created_at"))
        self.assertTrue(hasattr(model, "email"))
        self.assertTrue(hasattr(model, "password"))
        self.assertTrue(hasattr(model, "first_name"))
        self.assertTrue(hasattr(model, "last_name"))

    def test_var_initialization(self):
        """Check default type"""
        model = State()
        self.assertIsInstance(model.created_at, datetime)

    def test_save(self):
        """saving the object to storage"""
        test_user = {'id': "001",
                     'email': "you@g.com",
                     'password': "1234",
                     'first_name': "TEST",
                     'last_name': "REVIEW"}
        user = User(test_user)
        user.save()
        storage.delete(user)

if __name__ == "__main__":
    unittest.main()
