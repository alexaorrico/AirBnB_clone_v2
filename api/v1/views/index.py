#!/usr/bin/python3
"""a route to the index page"""

from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    status_dict = {"status": "OK"}
    return jsonify(status_dict)
