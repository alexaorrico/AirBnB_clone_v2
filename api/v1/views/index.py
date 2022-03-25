#!/usr/bin/python3
"""index file for api"""
import json

from flask import jsonify
from api.v1.views import app_views

@app_views.route('/status')
def status(text="is_cool"):
    """returns JSON status"""
    return jsonify({"status": "OK"})
