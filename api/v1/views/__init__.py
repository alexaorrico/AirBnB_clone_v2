#!/usr/bin/python3
"""Initialize the Blueprint for v1 views"""

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views import index  # Import the views module
