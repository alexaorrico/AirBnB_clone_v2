#!/usr/bin/python3
"""
    Script defines a route /status that
    returns a JSON response with the status "OK".
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def get_status():
    """ get status """
    return jsonify({"status": "OK"})
