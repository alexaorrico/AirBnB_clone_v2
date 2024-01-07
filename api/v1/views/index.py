#!/usr/bin/python3

from flask import jsonify
from api.v1.views import app_views

@app_views.route('/status', methods=['GET'])
def status():
    """Returns a JSON response with status OK"""
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'])
def stats():
    """Returns a JSON response with the count of objects"""
    total_objects = storage.count()
    return jsonify({"status": "OK", "count": total_objects})
