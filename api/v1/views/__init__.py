#!/usr/bin/python3
"""
This module initializes the Blueprint for version 1 of the AirBnB API.

It creates a Flask blueprint instance and imports the
views to include in the blueprint.

Example:
    from api.v1.views import app_views

    app.register_blueprint(app_views)

    # Other views can be imported here as needed

"""
from flask import Blueprint

# Create a blueprint instance for version 1 of the API
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
from api.v1.views.places_amenities import *