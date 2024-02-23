#!/usr/bin/python3
"""this module implements the views api"""
from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status')
def status():
    """returns the status of the api"""
    return jsonify({
        "status": "OK"
        })
