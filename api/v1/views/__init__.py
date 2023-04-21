#!/usr/bin/python3
"""Package initialization for the views module of v1 of the RESTful API"""

from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
