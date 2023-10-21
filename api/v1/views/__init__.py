#!/usr/bin/python3
"""
Initialization module to create the app_views Blueprint
"""
from flask import Blueprint

# Create a Blueprint instance with the URL prefix '/api/v1'
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
