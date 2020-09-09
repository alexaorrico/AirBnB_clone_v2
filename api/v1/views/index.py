#!/usr/bin/python3
"""
Module for routing of index
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def status():
    """ Returns JSON with status "OK" """
    return jsonify({"status": "OK"})
