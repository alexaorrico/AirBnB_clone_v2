#!/usr/bin/python3
"""
Package initializer for API v1 views.
"""

from flask import Blueprint
from os import path
from api.v1.views import *
import os

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# Automatic import of all modules in the current package
modules = [path.splitext(module)[0] for module in os.
           listdir(path.dirname(__file__)) if module != '__init__.py']
__all__ = modules
