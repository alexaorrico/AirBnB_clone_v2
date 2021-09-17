#!/usr/bin/python3
"""
script that starts a Flask web application:
"""

from api.v1.views import app_views
from flask import jsonify, request
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    return jsonify({'status': 'OK'})
