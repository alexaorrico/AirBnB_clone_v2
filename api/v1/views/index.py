#!/usr/bin/python3
""" Index route """
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Returns a JSON status response"""
    return jsonify({"status": "OK"})
