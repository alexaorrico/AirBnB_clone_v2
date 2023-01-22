#!/usr/bin/python3
"""Views init file"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")
state_views = Blueprint("state_views", __name__, url_prefix="/states")


from api.v1.views.index import *
from api.v1.views.states import *