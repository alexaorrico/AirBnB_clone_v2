#!/usr/bin/python3
"""Index view
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    """Status of the web server."""
    return jsonify({'status': 'OK'})


@app_views.route("/stats", methods=['GET'], strict_slashes=False)
def stats():
    """Stats from the storage."""
    classes = {
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review,
        "states": State,
        "users": User
    }
    return jsonify({k: storage.count(v) for k, v in classes.items()})
