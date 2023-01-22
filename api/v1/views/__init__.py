#!/usr/bin/python3
"""Endpoint (route) to return the status of api"""
from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
