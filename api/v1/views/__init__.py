#!/usr/bin/python3
from api.v1.views.index import *
from flask import Blueprint
"""
This module initializes the Blueprint for API version 1.
"""


# Create a Blueprint instance with URL prefix /api/v1
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Wildcard import (PEP8 will complain, but it's expected)
