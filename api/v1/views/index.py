#!/usr/bin/python3
"""
this file is used to output the json of the flask task
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def status():
    """Returns a JSON response with status 'OK'."""
    return jsonify({"status": "OK"})
