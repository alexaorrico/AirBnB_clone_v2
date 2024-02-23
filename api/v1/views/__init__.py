#!/usr/bin/python3
"""
Init file
"""
from flask import Blueprint

app_viewa = Blueprint('app_views', __name__, url_prefix='/api/v1')

"""wildcard import from index.py"""
from api.v1.views.index import *
