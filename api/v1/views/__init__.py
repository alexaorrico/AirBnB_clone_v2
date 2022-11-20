#!/usr/bin/python3
"""
Module for defining blueprint for routes
"""
from flask import Blueprint


app_views = Blueprint("app_views", __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.state import *
