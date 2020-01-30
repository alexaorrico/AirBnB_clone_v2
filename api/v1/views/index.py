#!/usr/bin/python3
"""
index route of the api
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """ returns status for the api """
    return jsonify({"status": "OK"})
