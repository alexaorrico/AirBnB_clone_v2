#!/usr/bin/python3
"""
Package initializer for app_views blueprint
"""
from flask import Blueprint

# define a blueprint
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# imports modules of app_views blueprint
from api.v1.views.index import *
from api.v1.views.states import *
