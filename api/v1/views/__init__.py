#!/usr/bin/python3
"""initialize a blueprint"""
from flask import Blueprint
# from flask_restful import Api

app_views = Blueprint("app_views", __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *

# api = Api(app_views)

# api.add_resource(State_view_all, "/states/")
# api.add_resource(State_view, "/states/<state_id>")
