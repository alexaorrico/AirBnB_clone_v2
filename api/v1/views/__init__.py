#!/usr/bin/python3
<<<<<<< HEAD
""" Blueprint for API """
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places_amenities import *
=======
"""
This is the __init__ module.

This module initializes the Flask application.
"""

from flask import Blueprint

# Create a Blueprint instance
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# Import all views from the index module
from api.v1.views.index import *
>>>>>>> 06b410135511d330f62384b22242c5fb082e4dc0
