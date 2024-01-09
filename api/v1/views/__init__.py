#!/usr/bin/python3
"""create views"""
import api.v1.views.index import *
import api.v1.views.states import *
import api.v1.views.cities import *
import api.v1.views.amenities import *
import api.v1.views.users import *
import api.v1.views.places import *

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix="/api/v1")
