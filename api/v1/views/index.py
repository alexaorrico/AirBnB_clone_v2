#!/usr/bin/python3
""" Create a route /status on the object app_views that
    returns a JSON: "status": "ok"
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/status', strict_slashes=False)
def get_status():
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def get_stats():
    from models import storage
    classes = [Amenity, City, Place, Review, State, User]
    # names = [c.__name__.lower() for c in classes]
    names = ["amenities", "cities", "places", "reviews", "states", "users"]
    stats = {}
    for name in range(len(classes)):
        stats[names[name]] = storage.count(classes[name])
    return jsonify(stats), 200
