#!/usr/bin/python3
'''Defines the app_views instance of Blueprint'''
from flask import Blueprint
from api.v1.views.index import *

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")
