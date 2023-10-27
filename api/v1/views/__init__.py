#!/usr/bin/python3
from flask import Blueprint
app_views = Blueprint(name='api', import_name=__name__, url_prefix="/api/v1")
from api.v1.views.index import *
