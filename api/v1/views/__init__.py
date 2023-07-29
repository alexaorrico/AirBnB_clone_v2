#!/usr/bin/python3
"""
__init__.py
This module creates a variable app_views which is an instance of Blueprint
"""

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
state_views = Blueprint('app_views', __name__, url_prefix='/api/v1/states')

from api.v1.views.index import *
from api.v1.views.states import *
