#!/usr/bin/python3
"""
    INIT BLUEPRINT AND 
    IMPORT VIEW
"""
from flask import Blueprint


app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")


# blueprint to import routes and state blueprints for CRUD and JSON - based
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *