#!/usr/bin/python3
"""default route"""
from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models import storage
from models.user import User


@app_views.route('/status', methods=["GET"], strict_slashes=False)
def status():
    """status of server"""
    return jsonify({
            "status": "OK"
        })


@app_views.route('/stats', methods=["GET"], strict_slashes=False)
def stats():
    """Count of each Object type"""
    all_name = ["amenities", "cities", "places", "reviews", "states", "users"]
    classes = [Amenity, City, Place, Review, State, User]
    all_count = {}
    for i in range(len(classes)):
        all_count[all_name[i]] = storage.count(classes[i])
    return jsonify(all_count)
