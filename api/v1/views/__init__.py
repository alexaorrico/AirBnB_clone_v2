#!/usr/bin/python3
"""creating a Blueprint instance; app_views"""

from flask import Blueprint

app_views= Blueprint("app_views", __name__, url_prefix="/api/v1")

