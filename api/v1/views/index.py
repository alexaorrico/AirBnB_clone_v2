#!/usr/bin/python3
"""ALX SE Flask Api Module."""
from flask import jsonify
from api.v1.views import app_views


# app_views = api.v1.views.app_views


@app_views.route('/status', strict_slashes=False)
def server_status():
    """Check if the server is online."""
    return jsonify({'status': 'OK'})
