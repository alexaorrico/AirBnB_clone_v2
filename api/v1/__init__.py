#!/usr/bin/python3
"""Blueprint for API v1 views"""

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views import index
from api.v1.views import states  # Import states view

# Import other view files as needed
