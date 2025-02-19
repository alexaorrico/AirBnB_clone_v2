#!/usr/bin/python3
"""api index"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status")
def status():
    """blueprints route"""
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stats():
    """number of each objects by type"""
    all_classes = {
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review,
        "states": State,
        "users": User
    }
    classes_count = {}
    for key, value in all_classes.items():
        classes_count[key] = storage.count(value)
    return jsonify(classes_count)
