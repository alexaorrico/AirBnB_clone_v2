#!/usr/bin/python3
"""
Module for create route in the object and return a JSON status Ok
"""

from flask import jsonify
from api.v1.views import app_views

@app_views.route('/status')
def jsonReturn():
    return jsonify({"status": "OK"})
