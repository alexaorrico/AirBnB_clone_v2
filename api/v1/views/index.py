#!/usr/bin/python3
""" index routes """
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
classes = {
    "amenities": Amenity,
    "cities": City,
    "places": Place,
    "reviews": Review,
    "states": State,
    "users": User,
}


@app_views.route("/status")
def get_status():
    """Status of my API"""
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def count_data():
    """count data"""
    total = {}
    for k, v in classes.items():
        total[k] = storage.count(v)
    return jsonify(total)
