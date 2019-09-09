#!/usr/bin/python3
"""function to create the route status"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """status render template for json"""
    return jsonify({"status": "OK"})
