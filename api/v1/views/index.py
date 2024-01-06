#!/usr/bin/python3
"""module for index blueprints"""

from api.v1.views import app_views
from flask import jsonify
from models import storage

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Returns status Ok"""
    return jsonify({"status": "OK"})

@app_views.route('/api/v1/stats', methods=['GET'],
                 strict_slashes=False)
def count():
    """Retrieves the number of objects"""
    obj_type = [Amenity, State, City, Review, Place, User]
    stats = {}
    for obj in obj_type:
        stats_result = storage.count(obj)
        stats[obj] = stats_result
    return jsonify(stats)
    
"""Includes Flask routes for airbnb clone"""

from api.v1.views import app_views
from flask import jsonify, request
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Returns status of API"""
    if request.method == 'GET':
        answer = ({"status": "OK"})
        return jsonify(answer)
