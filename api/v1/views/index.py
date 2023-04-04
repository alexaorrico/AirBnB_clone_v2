#!/usr/bin/python3
"""API Status and Statistics"""
from api.v1.views import app_views
from flask import Response, jsonify
from json import dumps
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status", methods=["GET"], strict_slashes=False)
def api_status():
    """
    Returns the status of the API
    """
    return Response(dumps({"status": "OK"}), content_type='application/json')


@app_views.route("/stats", methods=["GET"], strict_slashes=False)
def api_stats():
    """
    Returns the number of objects in each class
    """
    stats = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User),
    }
    return jsonify(stats)
