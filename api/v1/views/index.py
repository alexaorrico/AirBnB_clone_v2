#!/usr/bin/python3
"""
Contains app route for /status in the blueprint app_views
It returns an okay status code for the api
"""
from flask import jsonify
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
    """
    Returns the status of the api
    """
    return (jsonify({'status': 'OK'}))


@app_views.route("/stats", methods=["GET"])
def stats():
    """
    Returns the number of each object type
    """
    classes = {
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review,
        "states": State,
        "users": User
    }
    counts = {key: storage.count(value) for key, value in classes.items()}
    return jsonify(counts)
