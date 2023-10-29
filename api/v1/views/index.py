#!/usr/bin/python3
"""Index module"""

from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status")
def check_status():
    """Returns status of the flask app"""
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def fetch_stats():
    """Retrieve objects info from storage"""
    stats = {}
    stats['amenities'] = storage.count(Amenity)
    stats['cities'] = storage.count(City)
    stats['places'] = storage.count(Place)
    stats['reviews'] = storage.count(Review)
    stats['states'] = storage.count(State)
    stats['users'] = storage.count(User)

    return jsonify(stats)
