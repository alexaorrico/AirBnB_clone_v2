#!/usr/bin/python3
"""import blueprint"""
from api.v1.views.index import *
from flask import Blueprint

app_views = Blueprint('app_views', __name__)
