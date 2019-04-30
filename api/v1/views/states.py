#!/usr/bin/python3
from flask import jsonify
from models import storage
from api.v1.views import app_views


@app_views.route("/states", strict_slashes=False, methods=['GET'])
def state_get(state_id=None):
    """Handle GET request for states"""
    if state_id is None:
        pass