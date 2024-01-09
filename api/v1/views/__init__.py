#!/usr/bin/python3
"""Initialization of the Blueprint for API version 1 views"""
from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix="/api/v1")


from api.v1.views.index import *
