#!/usr/bin/python3
"""this module creates app_views which is an instance of Blueprint
"""
from api.v1.views.index import *
from flask import Blueprint


app_views = Blueprint('app_views', __name__)
