#!/usr/bin/python3
"""Script that creates the Blueprint Flask Class and import modules"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
