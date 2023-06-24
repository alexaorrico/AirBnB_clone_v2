#!/usr/bin/python3
"""Index module."""
from api.v1.views import app_views
from flask import jsonify
from models import storage


app_views.route("/status", url_prefix='/api/v1')


def get_status():
    """Status of api."""
    return jsonify(status="ok")



