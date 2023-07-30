#!/usr/bin/python3
"""The Blueprint for API module"""
from flask import Blueprint
from api.v1.views.index import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from views import states
from views import cities


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
