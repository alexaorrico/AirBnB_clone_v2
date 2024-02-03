# api/v1/views/__init__.py
"""
Package initializer for views in version 1 of the API.
"""
from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
from api.v1.views.states import app_views
