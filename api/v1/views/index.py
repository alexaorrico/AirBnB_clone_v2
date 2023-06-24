#!/usr/bin/python3
"""Create a status route."""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """Print 'ok' string."""
    return jsonify(status='OK')
