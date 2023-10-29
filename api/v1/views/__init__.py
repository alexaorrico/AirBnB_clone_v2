#!/usr/bin/python3

"""
create variable app_views - instance of Blueprint
"""


from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix="/api/v1")


from api.v1.views.index import *
