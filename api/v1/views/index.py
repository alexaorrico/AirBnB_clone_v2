#!/usr/bin/python3
"""Create a route /status on the object app_views"""
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Return a JSON"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def endpoint():
    """Create an endpoint"""
    stat = {}
    objs = {
        "Amenity": "amenities", "City": "cities",
        "Place": "places", "Review": "reviews",
        "State": "states", "User": "users"
    }
    for cls_name, key in objs.items():
        stat[key] = storage.count(eval(cls_name))

    return jsonify(stat)
