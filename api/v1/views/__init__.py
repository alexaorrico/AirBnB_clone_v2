#!/usr/bin/python3
"""Create a Flask Blueprint with a URL prefix"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Wildcard import of everything in package api.v1.views.index
from api.v1.views.index import *
from api.v1.views.states import *
