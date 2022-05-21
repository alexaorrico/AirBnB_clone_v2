#!/usr/bin/python3
"""
This is an init module that define define a blueprint
"""
from api.v1.views.places_reviews import *
from api.v1.views.users import *
from api.v1.views.cities import *
from api.v1.views.index import *
from flask import Blueprint

app_views = Blueprint('api', __name__, url_prefix='/api/v1')
