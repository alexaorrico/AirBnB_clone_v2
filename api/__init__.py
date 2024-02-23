#!/usr/bin/python3
"""
api/__init__.py
"""

from flask import Flask
app = Flask(__name__)

# Import views to register blueprints
from api.v1 import app_views

# Register blueprints
app.register_blueprint(app_views)
