#!/usr/bin/python3
"""
set the index path
"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route("/status", methods=["GET"], strict_slashes=False)
def status():
    """return  state in json"""
    return jsonify(status='OK')
