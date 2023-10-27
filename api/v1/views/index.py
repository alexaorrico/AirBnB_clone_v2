#!/usr/bin/python3
"""Index routes"""
from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Returns a JSON: 'status': 'OK'"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def stats():
    """Retrieve the number of each objects by type"""
    classes = {"amenities": Amenity, "cities": City, "places": Place,
               "reviews": Review, "states": State, "users": User}
    counts = {}
    for key, cls in classes.items():
        counts[key] = storage.count(cls)
    return jsonify(counts)
