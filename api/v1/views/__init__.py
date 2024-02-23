#!/usr/bin/python3
"""
api/v1/views/__init__.py
"""

from flask import Blueprint
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Import views
from api.v1.views import index
