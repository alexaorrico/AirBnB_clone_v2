#!/usr/bin/python3
"""this end point count number of each object"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """returns a JSON response"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """endpoint that retrieves the number of each objects by type"""
    classes = {
            "amenities": Amenity,
            "cities": City,
            "places": Place,
            "reviews": Review,
            "states": State,
            "users": User
            }
    dicts = {}
    for k, v in classes.items():
        num = storage.count(v)
        dicts[k] = num
    return jsonify(dicts)
