#!/usr/bin/python2
"""script to give status in JSON"""
from api.v1.views import app_views
from flask import request, jsonify

@app_views.route('/status', methods=['GET'])
def status_ok():
    """return JSON status ok"""
    return jsonify({"status": "OK"})
