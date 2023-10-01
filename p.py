#!/usr/bin/python3
""" Test .get() and .count() methods
"""
from models.base_model import BaseModel


a = BaseModel()
b = BaseModel()
c = BaseModel()

print(a.created_at)
print(b.created_at)
print(c.created_at)
