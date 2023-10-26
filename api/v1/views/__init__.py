#!/usr/bin/python3
"""blueprint"""
from api.v1.views.index import *
from flask import Blueprint
app_views = Blueprnt("app_views", __name__, url_prefix='/api/v1')
