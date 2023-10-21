#!/usr/bin/python3
"""
Index module
"""
from flask import jsonify
from api.v1.views import app_views

@app_views.route('/status', methods=['GET'])
def status():
    """
    Returns status: OK in JSON format
    """
    return jsonify({"status": "OK"})
