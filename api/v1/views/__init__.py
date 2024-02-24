#!/usr/bin/python3
"""
    import Blueprint from flask doc
"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

if not __debug__:
    from api.v1.views.index import *
