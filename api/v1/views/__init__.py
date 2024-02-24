#!/usr/bin/python3
"""
Init file
"""
from flask import Blueprint


"""Create a Blueprint instance with URL prefix /api/v1"""
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

"""of everything in the index.py module"""
from .index import *
