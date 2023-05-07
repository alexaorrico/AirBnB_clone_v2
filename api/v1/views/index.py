#!/usr/bin/python3
"""
views blueprint routes
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


@app_views.route("/status", strict_slashes=False)
def api_status():
    """/status endpoint

    Returns:
        json: a status OK message
    """
    return jsonify(status="OK")


@app_views.route("/stats", strict_slashes=False)
def api_stats():
    """/stats endpoint

    Returns:
        json: stats on all saved data
    """
    stats = {
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review,
        "states": State,
        "users": User
    }

    for stat in stats:
        stats[stat] = storage.count(stats[stat])

    return jsonify(stats)
