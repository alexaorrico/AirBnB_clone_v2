#!/usr/bin/python3
""" A module defines a rule that returns the current state of the app """
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """ This function returns the app's status as JSON. """
    return jsonify({"status": "OK"})
