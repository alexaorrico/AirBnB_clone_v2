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


@app_views.route('/status')
def status():
    return jsonify({
            "status": "OK"
        })


@app_views.route('/stats', methods=["GET"])
def count():
    """Count of each Object type"""
    all_name = ["amenities", "cities", "places", "reviews", "states", "users"]
    all_type = [Amenity, City, Place, Review, State, User]
    all_count = {}
    for i in range(len(all_type)):
        all_count[all_name[i]] = storage.count(all_type[i])
    return jsonify(all_count)
