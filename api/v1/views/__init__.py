#!/usr/bin/python3
"""Imports the Blueprint"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

"""Imports flask views"""
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
