#!/usr/bin/python3
"""
This is the __init__ module.

This module initializes the Flask application.
"""

from flask import Blueprint

# Create a Blueprint instance
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# Import all views from the index module
from api.v1.views.index import *
