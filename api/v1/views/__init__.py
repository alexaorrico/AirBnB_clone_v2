#!/usr/bin/python3
from api.v1.views.index import *
from flask import Blueprint
from api.v1.views import states
from api.v1.views import cities

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
