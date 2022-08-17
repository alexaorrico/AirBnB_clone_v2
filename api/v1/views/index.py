#!/usr/bin/python3
"""Routes status on the object app_views"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """returns jsonify status"""
    return jsonify(status="OK")
