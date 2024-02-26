#!/usr/bin/python3
"""
routes
"""

# api/v1/views/index.py
from flask import jsonify, Blueprint

app_views = Blueprint('app_views', __name__)


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Returns the status of the API"""
    return jsonify({"status": "OK"})
