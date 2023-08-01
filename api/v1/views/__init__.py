#!/usr/bin/python3
<<<<<<< HEAD
"""Initialize Blueprint views"""
=======
"""Contains the blueprint for the API."""
>>>>>>> f61419b9c8d53faeeaab2f7b00854c945df71058
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

<<<<<<< HEAD
from api.v1.views.index import *
from api.v1.views.amenities import *
from api.v1.views.cities import *
from api.v1.views.places import *
from api.v1.views.places_amenities import *
from api.v1.views.places_reviews import *
from api.v1.views.states import *
from api.v1.views.users import *
=======
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
"""The blueprint for the AirBnB clone API."""


from api.v1.views.index import *
>>>>>>> f61419b9c8d53faeeaab2f7b00854c945df71058
