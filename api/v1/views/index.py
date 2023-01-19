#!/usr/bin/python3

from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status')
def status_api():
    """Returning API status"""
    return (jsonify({"status": "OK"}))
