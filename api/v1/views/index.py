#!/usr/bin/python3
"""API main routes"""

from flask import jsonify

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"amenities": Amenity, "cities": City,
           "places": Place, "reviews": Review, "states": State, "users": User}


@app_views.route("/status", strict_slashes=False)
def status():
    """Returns the status in JSON format"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def stats():
    """Endpoint that retrieves the number of each objects by type"""
    stats_dict = {}
    for cls_name, cls in classes.items():
        stats_dict[cls_name] = storage.count(cls)
    return jsonify(stats_dict)
