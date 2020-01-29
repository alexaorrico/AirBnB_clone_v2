#!/usr/bin/python3
from api.v1.views import app_views
from json import dumps
from flask import jsonify
"""
index route of the api
"""

@app_views.route('/status')
def status():
    """ returns status for the api """
    return jsonify({"status": "OK"})
