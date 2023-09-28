#!/usr/bin/python3
"""the init file for views module"""
from flask import Blueprint
app_views = Blueprint(import_name=__name__, name="ty", url_prefix="/api/v1")
from api.v1.views.index import *
