#!/usr/bin/python3
"""Init file for views"""
from flask import Blueprint
from api.v1.views.index import *

app_views = Blueprint('api_views', __name__, url_prefix='/api/v1')
