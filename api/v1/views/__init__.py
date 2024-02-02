#!/usr/bin/python3
"""Handles configurations"""

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Import views to register the routes
from api.v1.views import *
