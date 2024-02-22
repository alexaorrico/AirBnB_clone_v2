#!/usr/bin/python3
"""
api flask app
"""
from flask import Blueprint
from api.v1.views.index import *

app_views = Blueprint('app_views', url_prefix="/api/v1")
