#!/usr/bin/python3
""" Initializes the api """
from flask import Blueprint

app_views = Blueprint('api_v1', __name__, url_prefix='/api/v1')
from api.v1.views.index import *
from api.v1.views.amenities import *
from api.v1.views.states import *
from api.v1.views.users import *
