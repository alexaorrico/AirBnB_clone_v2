#!/usr/bin/python3
"""
Module for initializing Flask Blueprint object
"""

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
