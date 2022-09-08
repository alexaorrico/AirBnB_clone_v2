#!/usr/bin/python3
"""index"""
from api.v1.views import app_views
from flask import jsonify, request


@app_views.route('/status')
def status():
    return jsonify({"status": "OK"})
