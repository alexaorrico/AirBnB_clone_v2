#!/usr/bin/python3
"""
This module initializes the Blueprint for the API views
"""
from flask import Blueprint

"""Create a Blueprint instance for the API views with specified URL prefix """
app_views = Blueprint('app_views', __name__, url_prefix="/api/v1")

""" import all the views module to register their  routes with Blueprint"""
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.amenities import *
from api.v1.views.cities import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
from api.v1.views.users import *
