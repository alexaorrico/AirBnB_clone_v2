#!/usr/bin/python
"""Define a blueprint for the API v1"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Pep8 doesn't like the next line, project said it's okay
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *