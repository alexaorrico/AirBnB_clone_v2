#!/usr/bin/python3
"""
Tasks 4, 7-12
Import app_views
"""
from flask import Blueprint
app_views = Blueprint('app_views', __name__, template_folder='templates')
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
