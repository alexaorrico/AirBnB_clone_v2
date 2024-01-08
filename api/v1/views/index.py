#!/usr/bin/python3
"""This file returns the JSON status ok"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def index():
    return jsonify({"status": "OK"})
