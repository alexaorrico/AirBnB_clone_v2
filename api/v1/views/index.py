#!/usr/bin/python3
"""Flask App"""


from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """test status OK"""
    return jsonify({"status": "OK"})
