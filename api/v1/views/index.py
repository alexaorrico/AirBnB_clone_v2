#!/usr/bin/python3
"""Includes Flask routes for airbnb clone"""

from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from models.review import Review
from models.amenity import Amenity

classes = {"amenities": Amenity, "cities": City,
           "places": Place, "reviews": Review, "states": State, "users": User}


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Returns status of API"""
    if request.method == 'GET':
        answer = ({"status": "OK"})
        return jsonify(answer)


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def count_stats():
    """Returns count of each object by type in JSON format"""
    if request.method == 'GET':
        answer = {}
        for key, value in classes.items():
            answer[key] = storage.count(value)
        return jsonify(answer)
