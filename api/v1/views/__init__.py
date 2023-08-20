#!/usr/bin/python3

from flask import Blueprint
"""
create a route /status on the object app_views
that returns a JSON: "status": "OK"
"""
from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1') 


from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
