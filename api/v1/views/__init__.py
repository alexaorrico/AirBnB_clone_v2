#!/usr/bin/python3
# api/v1/views/__init__.py

""" Initialization of Flask Blueprint for API views
"""

from flask import Blueprint


# Create a Blueprint named 'app_views' with a URL prefix '/api/v1'
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Import views from the 'index' module to include in the Blueprint
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
