#!/usr/bin/python3
"""
This module defines a Flask blueprint for handling status requests.
"""

from flask import jsonify
from . import app_views
from models import storage

@app_views.route('/api/v1/stats', methods=['GET'])
def get_status():
    counts = {}
    classes = storage.classes()
    for cls in classes:
        counts[cls] = storage.count(cls)

    return jsonify(counts), 200
