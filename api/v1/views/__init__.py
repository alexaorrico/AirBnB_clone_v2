#!/usr/bin/python3
"""Views definition?"""
from flask import Blueprint
from api.v1 import views

app_views = Blueprint('/api/v1', __name__)
