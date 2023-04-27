#!/usr/bin/python3
""" An index file for our Flask API """

from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status', strict_slashes=False)
def api_status():
    """ A function to return status of the API """
    return jsonify({"status": "OK"})
