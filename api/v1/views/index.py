#!/usr/bin/python3
""" Set up response for status code """
from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models import storage
from models.user import User


@app_views.route("/status")
def response_status():
    """ Return status of the API """
    return jsonify({"status": "OK"})

@app_views.route("/api/v1/stats", method=['GET'])
def get_object_stats():
    """Retrieves the number of each object in storage by type"""
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
