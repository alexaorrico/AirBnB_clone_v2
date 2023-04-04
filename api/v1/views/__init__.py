#!/usr/bin/python3
"""Define a blueprint for the API v1"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.cities import *
from api.vi.views.states import *
