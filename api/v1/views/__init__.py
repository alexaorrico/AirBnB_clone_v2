#!/usr/bin/python3
"""the init file for this package
"""
from api.v1.views.index import *
from flask import Blueprint

app_views = Blueprint('app_views', __name__)
