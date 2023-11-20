#!/usr/bin/python3
""" Blueprint """
# Michael edited 11/19 8:21 PM

from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

from api.v1.views.index import *
