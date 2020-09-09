#!/usr/bin/python3
"""connect to api"""

from api.v1.views import app_views
from flask import jsonify, Flask, Blueprint


@app_views.route('/status', strict_slashes=False)
def objStatus():
    """return the status"""
    return jsonify({"status": "OK"})
