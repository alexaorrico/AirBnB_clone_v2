#!/usr/bin/python3
"""
module for views end points using Blueprint
"""
from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
