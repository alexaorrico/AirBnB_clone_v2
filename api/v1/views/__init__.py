#!/usr/bin/python3
"""This module contains a flask blueprint for a web application"""

from flask import Blueprint
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# import all blueprints that uses the app_views
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
