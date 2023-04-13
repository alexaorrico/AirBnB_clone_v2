#!/usr/bin/python3
<<<<<<< HEAD
"""
api status page Blueprint package
containing 'flask.Blueprint' object 'app_views'
"""
from flask import Blueprint
import api.v1.views.states

app_views = Blueprint(
    "api_status_page",
    __name__,
    url_prefix="/api/v1"
)

from api.v1.views.index import *
=======
""" __init__ module for app_views"""
from flask import Blueprint, Flask, abort, render_template

app_views = Blueprint('app_views', __name__, url_prefix="/api/v1")

from api.v1.views.index import *
>>>>>>> master
