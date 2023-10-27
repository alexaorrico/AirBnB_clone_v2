#!/usr/bin/python3
"""
__init__ File that defines views folder content
as a package (it will be used for Flask)
"""
from flask import Blueprint
app_views = Blueprint("app_views", __name__, url_prefix='/api/v1')
# task 3
from api.v1.views.index import *
