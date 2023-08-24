#!/usr/bin/python3
""" Init file """

from flask import Blueprint
from api.v1.views.states import *
from api.v1.views.cities import *
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
