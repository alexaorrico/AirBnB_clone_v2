#!/usr/bin/python3
"""Returns JSON status"""
from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


@app_views.route("/status", methods=["GET"], strict_slashes=False)
def status():
    """Returns the status of our API"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=["GET"], strict_slashes=False)
def count_objects():
    """Counts the number of objects by type"""
    classes = [Amenity, City, Place, Review, State, User]
    names = ["amenities", "cities", "places", "reviews", "states", "users"]

    num_obj = {}
    for i in range(len(classes)):
        num_obj[names[i]] = storage.count(classes[i])

    return jsonify(num_obj)
