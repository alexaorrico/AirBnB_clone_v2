#!/usr/bin/python3
"""Defines a Flask route"""
from flask import jsonify, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', methods=['GET'])
def status():
    """Returns a JSON response with the status OK"""
    return jsonify({"status": "OK"})


classes = {"amenities": Amenity, "cities": City,
           "places": Place, "reviews": Review, "states": State, "users": User}


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def count_stats():
    """Returns count of each object by type in JSON format"""
    if request.method == 'GET':
        answer = {}
        for key, value in classes.items():
            answer[key] = storage.count(value)
        return jsonify(answer)
