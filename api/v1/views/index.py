#!/usr/bin/python3
"""Modules for handling routes stats and general status."""
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/stats')
def stats():
    """Restores numbers for each object by type."""
    classes_dict = {"amenities": Amenity, "cities": City, "reviews": Review, "states": State, "users": User}
    counter_dict = {}
    for key, value in classes_dict.items():
        counter_dict[key] =storage.count(value)
        return jsonify(counter_dict)


@app_views.route('/status')
def status():
    """Returns OK."""
    return jsonify({"status": "OK"}), 200
