#!/usr/bin/python3
""" """
import unittest
from time import sleep

import env
from models.user import User
from tests.test_models.test_base_model import test_basemodel


class test_User(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "User"
        self.value = User

    def test_first_name(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.first_name), type(None))

    def test_last_name(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.last_name), type(None))

    def test_email(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.email), type(None))

    def test_password(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.password), type(None))


@unittest.skipIf(not env.DBTYPE, "not testing file storage")
class test_User_db(unittest.TestCase):
    """
    Test the User class with DBStorage
    """
    session = None

    def setUp(self) -> None:
        from models import storage
        self.session = storage.get_session()
        self.session.query(User).delete()
        self.session.commit()

    def tearDown(self) -> None:
        self.session.query(User).delete()
        self.session.commit()

    def test_save(self):
        """
        Test save method
        """
        before = self.session.query(User).count()
        new = User(email="test@gmail.com", password="test",
                         first_name="test", last_name="test")
        new.save()
        after = self.session.query(User).count()
        self.assertEqual(before + 1, after)
