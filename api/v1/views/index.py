#!/usr/bin/python3
"""Defining the modulee"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Method that returns the status"""

    return jsonify({
                    "status": "OK"
                    })
