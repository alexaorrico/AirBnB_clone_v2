#!/usr/bin/python3
"""
initializes the api views from a flask blueprint set up in api/v1/app.py
"""

from flask import Blueprint
from api.v1.views.index import *

app_views = Blueprint()  # (url prefix must be /api/v1)
