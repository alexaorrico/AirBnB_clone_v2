#!/usr/bin/python3
"""Views init Docstring"""
from flask import Blueprint


# Does static folder also need to be set?
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
from api.v1.views.index import *
