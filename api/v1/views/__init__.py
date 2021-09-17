#!/usr/bin/python3
"""Is the Status of your API"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
