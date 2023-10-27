#!/usr/bin/python3
"""
index.py File that defines a view function
on route  "/status"
"""
from flask import jsonify
from api.v1.views import app_views
# create a route /status on the object app_views
# that returns a JSON: "status": "OK"


@app_views.route('/status', strict_slashes=False)
def get_app_status():
    """ return status ok in json
    """
    return(jsonify({"status": "OK"}))
