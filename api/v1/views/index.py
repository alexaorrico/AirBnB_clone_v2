#!/usr/bin/python3
""" api/v1/views/index.py """
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

@app_views.route("/stats")
def stats():
    """Return a JSON with the number of each objects by type"""
    classes = {
        "users": User,
        "states": State,
        "cities": City,
        "amenities": Amenity,
        "places": Place,
        "reviews": Review
    }
    stats = {}
    for key, value in classes.items():
        stats[key] = storage.count(value)
    return jsonify(stats)
