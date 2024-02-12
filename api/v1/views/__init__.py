#!/usr/bin/python3
"""the init module executes whenever the views module is imported"""
from flask import Blueprint


app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

from .index import *
