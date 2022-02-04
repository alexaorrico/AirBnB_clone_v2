#!/usr/bin/python3
"""
Script that starts a Flask web application
"""
from flask import Blueprint
import api.v1.views.index

app_views = Blueprint(url_prefix='/api/v1')
