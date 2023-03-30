#!/usr/bin/python
"""Define a blueprint for the API v1"""
from flask import Blueprint
# Pep8 doesn't like the next line, project said it's okay
from api.v1.views.index import *

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
