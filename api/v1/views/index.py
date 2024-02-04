#!/usr/bin/python3
"""
This module contains the index
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
classes = {"amenities": Amenity, "cities": City, "places": Place,
           "reviews": Review, "states": State, "users": User}


@app_views.route('/status', strict_slashes=False)
def api_status():
    """returns the status of the api"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """returns the stats of all classes"""
    stats_dict = {k: storage.count(v) for k, v in classes.items()}
    return jsonify(stats_dict)
