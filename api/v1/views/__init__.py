#!/usr/bin/python3
"""Initialize views blueprint"""
from flask import Blueprint

app_views = Blueprint("base", __name__, url_prefix="/api/v1")

# Import views
from api.v1.views.amenities import *
from api.v1.views.cities import *
from api.v1.views.index import *
from api.v1.views.places import *
from api.v1.views.places_amenities import *
from api.v1.views.places_reviews import *
from api.v1.views.states import *
from api.v1.views.users import *
