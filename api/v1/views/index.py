#!/usr/bin/python3
"""
Creates a routes on the object
"""

from api.v1.views import app_views
from flask import jsonify

# We define a route on app_view object
@app_views.route('/status')
def status():
    """ returns a JSON status """
    return jsonify({"status": "OK"})
