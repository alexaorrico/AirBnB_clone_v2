#!/usr/bin/python3
"""
File to initialize for the views module
"""
from flask import Blueprint

# Create a Blueprint instance with URL prefix '/api/v1'
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1/')

from api.v1.views.index import *
from api.v1.views.states import *