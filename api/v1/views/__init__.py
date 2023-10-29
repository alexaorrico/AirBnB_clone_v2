#!/usr/bin/python3
""" This module defines a Flask blueprint for creating routes. """
from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# wildcard import of everything in the package api.v1.views.index
from api.v1.views.index import *
