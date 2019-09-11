#!/usr/bin/python3
"""
initialize Blueprint
"""

from flask import Blueprint


app_views = Blueprint("mold", __name__, url_prefix='/api/v1')
