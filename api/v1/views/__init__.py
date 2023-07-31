#!/usr/bin/python3
"""
Creates a Blueprintinstance with url prefix = /api/v1
"""

from flask import Blueprint


app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")


"""import flask views"""
from api.v1.views.index import *
from api.v1.views.states import *
