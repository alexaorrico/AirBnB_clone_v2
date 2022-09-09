#!/usr/bin/python3
"""init"""
from flask import Blueprint
app_views = Blueprint('api', __name__, url_prefix='/api/v1')
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.amenities import *
