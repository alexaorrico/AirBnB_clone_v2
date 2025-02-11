#!/usr/bin/python3
# Author: Joana Casallas
"""Index API"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def status():
    """Return API status"""
    return jsonify({"status": "OK"})
