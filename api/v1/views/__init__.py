#!/usr/bin/python3
""" This module initializes the blueprint app_views """

from flask import Blueprint

# Create a variable named app_views
# which is an instance of class Blueprint
# the URL prefix will be /api/v1
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# Wildcard import to import all modules
# in the directory api/v1/views
# The file api/v1/views/__init__.py is called a package
# and the directory api/v1/views is called a subpackage
# Path: api/v1/views/__init__.py
# This file (v1/views/__init__.py) won’t be checked for PEP8 issues
from api.v1.views.index import *
from api.v1.views.states import *
