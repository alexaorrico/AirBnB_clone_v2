#!/usr/bin/python3
"""Index views"""


from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """A function return the status of the server"""
    app_status = {"status": "OK"}
    return jsonify(app_status)
