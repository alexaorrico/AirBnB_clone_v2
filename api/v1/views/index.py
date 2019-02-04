#!/usr/bin/python3
"""
Creates a route on the object app_views that returns a JSON
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """ Returns a JSON """
    return jsonify({'status': 'OK'})
