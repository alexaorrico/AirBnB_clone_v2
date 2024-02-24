#!/usr/bin/python3
"""
__init__.py is a special Python file that is used to define a package in Python.
"""

from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

from api.v1.views.index import *
