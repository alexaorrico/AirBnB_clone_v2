#!/usr/bin/python3
"""
Starts a Flask web app
"""
from flask import Blueprint
#from api.v1.views.index import *

app_views = Blueprint('app_views', '__name__', url_prefix='/api/v1')
from api.v1.views.index import *
from api.v1.views import states
