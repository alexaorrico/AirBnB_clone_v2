#!/usr/bin/python3
""" Create a route /status on the object app_views that
    returns a JSON: "status": "ok"
"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def get_status():
    return jsonify({"status": "OK"})
