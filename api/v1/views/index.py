#!/usr/bin/python3
"""Definition of index"""
from api.v1.views import app_views
from flask import Flask


@app_views.route('/status')
def status():
    """Returns status of App"""
    return jsonify({"status": "OK"})
