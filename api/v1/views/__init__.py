#!/usr/bin/python3
"""
The init for Blueprint
"""
from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
"""This is for api blueprint"""


from api.v1.views.index import *
