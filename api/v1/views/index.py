#!/usr/bin/python3
""" creates a route for the status """
from flask import jsonify
from api.v1.views import app_views


@app_views.route("/status", strict_slashes=False)
def status():
    """ Register the route """

    return jsonify({"status": "OK"})
