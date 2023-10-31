#!/usr/bin/python3
"""Flask route for index model"""

from api.v1.views import app_views
from flask import request, jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


classes = {"amenities": Amenity, "cities": City,
           "places": Place, "reviews": Review, "states": State, "users": User}


@app_views.route("/status", methods=["GET"])
def index():
    """request status route"""
    if request.method == "GET":
        return jsonify({"status": "OK"})


@app_views.route("/stats", methods=["GET"])
def stats():
    """an endpoint that retrieves the number of each objects by type:"""
    if request.method == "GET":
        names = [
                "amenities", "cities", "places", "reviews", "states", "users"
                ]
        result = {}
        for i in range(len(names)):
            name = names[i]
            result[name] = storage.count(classes[name])
        return jsonify(result)
