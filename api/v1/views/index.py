#!/usr/bin/python3
""" Index script """
from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


@app_views.route('/status', methods=['GET'],
                 strict_slashes=False)
def status():
    """Returns a JSON with status "OK"."""
    return jsonify(status="OK")


@app_views.route('/stats', strict_slashes=False)
# This code has the advantage of not returning non-existing objects
def stats():
    """display the number of each objects by type"""
    all_classes = {"Amenity": "amenities", "City": "cities", "Place": "places",
                   "Review": "reviews", "State": "states", "User": "users"}
    return jsonify({v: storage.count(k) for k, v in all_classes.items()
                    if storage.count(k)})
