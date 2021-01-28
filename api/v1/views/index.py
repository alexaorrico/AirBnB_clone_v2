#!/usr/bin/python3
"""Our first API"""


from flask import Flask
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """Route on the object app_views that returns a JSON"""
    return jsonify({"status": "OK"})
