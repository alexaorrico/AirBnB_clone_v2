#!/usr/bin/python3
""" In this module are the /status Blueprint"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """ return status """
    return jsonify({'status': "OK"})
