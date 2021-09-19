#!/usr/bin/python3
"""this module has route /status
"""
from flask import Flask, jsonify
from api.v1.views import app_views

@app_views.route('/status', strict_slashes=False)
def return_json():
    """return a JSON: 'status': 'OK'"""
    data = {"status": "OK"}
    return jsonify(data)
