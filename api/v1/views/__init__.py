#!/usr/bin/python3
"""Init file for v1.views"""

from flask import Blueprint

app_views = Blueprint("views", __name__)

from index import *
