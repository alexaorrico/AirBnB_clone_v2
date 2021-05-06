#!/usr/bin/python3
from models.amenity import Amenity
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User
from api.v1.views import app_views
from flask import Flask, jsonify


@app_views.route('/status', strict_slashes=False)
def route_status():
    return jsonify({"status": "OK"})

@app_views.route('/stats', strict_slashes=False)
def statsRoute():
    dircount = {}
    dir_clases = {
        "amenities": "Amenity",
        "cities": "City",
        "places": "Place",
        "reviews": "Review",
        "states": "State",
        "users": "User"
    }
    for key, value in dir_clases.items():
        dircount[key] = storage.count(value)
    return jsonify(dircount)

if __name__ == "__main__":
    pass