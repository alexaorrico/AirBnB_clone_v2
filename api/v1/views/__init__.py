#!/usr/bin/python3
"""
api status page Blueprint package
containing 'flask.Blueprint' object 'app_views'
"""
from flask import Blueprint, Flask, abort, render_template

app_views = Blueprint('app_views', __name__, url_prefix="/api/v1")

from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
