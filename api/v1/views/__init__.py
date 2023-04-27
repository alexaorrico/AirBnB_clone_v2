#!/usr/bin/python3
"""register the blueprint app_views to your Flask instance app"""


from flask import Blueprint
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


from api.v1.views.index import *
