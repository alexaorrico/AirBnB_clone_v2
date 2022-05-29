#!/usr/bin/python3
"""
Module which initializes BluePrint
"""

from api.v1.views.index import *
from flask import Blueprint

app_views = Blueprint("route", __name__, url_prefix='/api/v1')
