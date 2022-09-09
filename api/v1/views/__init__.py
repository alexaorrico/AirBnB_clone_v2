#!/usr/bin/python3
"""It's time to start your API. Your first endpoint\
(route) will be to return the status of your API"""


from api.v1.views.index import *
from flask import Blueprint

app_views = Blueprint("app_views", __name__, urlprefix=/api/v1)
