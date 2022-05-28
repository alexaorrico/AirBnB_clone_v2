#!/usr/bin/python3

""" create a route /status on the object app_views that returns a
    JSON: "status": "OK
"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
from api.v1.views.index import *
