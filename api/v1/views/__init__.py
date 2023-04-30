#!/usr/bin/python3
"""
The init file
"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix='/api/v1')

"""Now import flask views"""
from api.v1.views.index import *
