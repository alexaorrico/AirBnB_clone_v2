#!/usr/bin/python3
"""Task 0"""
from api.v1.views import app_views
from models import storage
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def Index():
    """Function index"""
    return jsonify({"status": "OK"})

@app_views.route('/api/v1/stats', methods=['GET'])
def number_objects():
    numb = storage.count()
    return jsonify({"objects": numb})
