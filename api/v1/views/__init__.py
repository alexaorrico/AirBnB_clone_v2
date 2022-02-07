#!/usr/bin/python3
"""
smth blueprint smth
"""
from flask import Blueprint
from api.v1.views.index import *
app_views = Blueprint('__init__', __name__, url_prefix='/api/v1')