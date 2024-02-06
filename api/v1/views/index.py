#!/usr/bin/python3
""" The implementation of blueprint for index routing behaviour"""
from flask import jsonify
from api.v1.views import app_views

from models import storage


@app_views.route("/status")
def status():
    """Function to reveal the status of API"""
    from flask import jsonify

    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stats():
    """Function to retrieve the stats of the built in
    API"""
    from models.amenity import Amenity
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models.user import User

    class_names = {
        Amenity: "amenities", City: "cities", Place: "places",
        Review: "reviews", State: "states", User: "users"

    }
    class_counts = {
        Amenity: 0, City: 0, Place: 0,
        Review: 0, State: 0, User: 0
    }

    for cls in class_counts.keys():
        class_counts[cls] = storage.count(cls)

    return jsonify({class_names[k]: v for k, v in class_counts.items()})
