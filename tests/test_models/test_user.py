#!/usr/bin/python3
""" """
import unittest

from tests.test_models.test_base_model import TestBaseModel
from models.user import User


class TestUser(TestBaseModel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "User"
        self.value = User

    def test_first_name(self):
        """ """
        new = self.value()
        new.first_name = "luffy"
        self.assertEqual(type(new.first_name), str)

    def test_last_name(self):
        """ """
        new = self.value()
        new.last_name = "monkey"
        self.assertEqual(type(new.last_name), str)

    def test_email(self):
        """ emtpy comment"""
        new = self.value()
        new.email = "monkey@deyluffy.com"
        self.assertEqual(type(new.email), str)

    def test_password(self):
        """ no comment """
        new = self.value()
        new.password = "no_monkey"
        self.assertEqual(type(new.password), str)
