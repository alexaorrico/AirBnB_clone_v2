#!/usr/bin/python3
"""API test stats"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """status"""
    return jsonify({"status": "OK"})
