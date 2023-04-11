#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify
""" index """


@app_views.route('/status', strict_slashes=False)
def status():
    """ return the status of the API """
    return jsonify({"status": "OK"})