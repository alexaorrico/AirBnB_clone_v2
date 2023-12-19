#!/usr/bin/python3
""" Blueprint for our API """


# api/v1/views/__init__.py
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Wildcard import for circular dependency (PEP8 will complain, but it's intentional)
from api.v1.views.index import *
