#!/usr/bin/python3
"""
creation of the blue print of the project
"""
from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
