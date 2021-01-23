#!/usr/bin/python3

from flask import Blueprint

# no idea if this is actually right
app_views = Blueprint("app_views", __name__, url_prefix="/ap1/v1")

from api.v1.views.index import *
