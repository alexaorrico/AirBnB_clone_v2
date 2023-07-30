#!/usr/bin/python3
""" Blueprint for API """
from flask import Blueprint

app_views = Blueprint('app_views', __name__, urlprefix='api/v1/')

from api.v1.views.cities import *
