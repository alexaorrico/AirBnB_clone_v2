#!/usr/bin/python3
"""
API Bleuprint Module

Initializes the Flask Blueprint for API views and sets up the URL prefix
for version 1 of the API.

Import the view(s) to include in the blueprint
"""

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
