#!/usr/bin/python3
from . import *
from flask import Blueprint
# from . import states

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Wildcard import of everything in the package api.v1.views.index
