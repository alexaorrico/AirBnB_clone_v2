#!/usr/bin/python3
""" Test .get() and .count() methods
"""
from models.user import User
from models import storage

users = [user.id for user in storage.all(User).values()]
print(users)