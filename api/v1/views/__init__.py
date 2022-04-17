#!/usr/bin/python3
"""view init file"""
from flask import Blueprint
from api.v1.views import states

app_views = Blueprint('index', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.cities import *
