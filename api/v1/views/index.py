#!/usr/bin/python3

from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Return the status of the server."""
    return jsonify(status="OK")
