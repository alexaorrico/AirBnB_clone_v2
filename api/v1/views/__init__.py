#!/usr/bin/python3
"""Blueprint setup"""

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Import routes so they are registered with the Blueprint
from api.v1.views.index import *
from api.v1.views.states import *
