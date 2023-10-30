#!/usr/bin/python3
"""
  View blueprint declaration
"""
from flask import Blueprint

app_views = Blueprint(__name__, url_prefix="/api/v1")

from api.v1.views.index import *
