#!/usr/bin/python3
"""This module is responsible for creating the necessary blueprint."""
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix='/api/v1')

if app_views:
    from api.v1.views.index import *
    from api.v1.views.states import *
    from api.v1.views.city import *
