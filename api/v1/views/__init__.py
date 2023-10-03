#!/usr/bin/python3
"""create blueprint"""
from flask import Blueprint
import os

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Dynamically import views from submodules
modules = [
    'index',
    'states',
    'cities',
    'amenities',
    'users',
    'places',
    'places_reviews',
    'places_amenities'
]

for module in modules:
    try:
        __import__('api.v1.views.' + module)
    except ImportError:
        pass
