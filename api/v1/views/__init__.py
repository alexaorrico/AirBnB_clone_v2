#!/usr/bin/python3
"""
This module defines the main Blueprint for the API views.
"""

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from . import index, states, cities, amenities, users, places
