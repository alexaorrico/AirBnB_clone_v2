#!/usr/bin/python3
"""documented module"""

from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    """retuens the status"""
    status = {"status": "OK"}
    return jsonify(status)


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    """ retrieves the number of each objects by type"""
    from models import storage
    stats = {}
    classes = {
              "Amenity": "amenities",
              "City": "cities",
              "Place": "places",
              "Review": "reviews",
              "State": "states",
              "User": "users"
              }
    for key, value in classes.items():
        stats[value] = storage.count(key)
    return jsonify(stats)
