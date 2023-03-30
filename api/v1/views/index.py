#!/usr/bin/python3
"""Create a route on the object app_views that returns a JSON: "status":OK """
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """Returns a JSON status"""
    return jsonify(status="OK")
