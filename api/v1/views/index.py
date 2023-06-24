#!/usr/bin/python3
"""Index."""
from api.v1.views import app_views
from flask import jsonify


app_views.route("/status")


def get_status():
    """Status of api."""
    return jsonify(status="ok")
