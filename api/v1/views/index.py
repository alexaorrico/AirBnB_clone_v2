#!/usr/bin/python3
""" Index view
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


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Return the status of the web server."""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """Return the number of each objects by type."""
    response = {}
    response['amenities'] = storage.count(Amenity)
    response['cities'] = storage.count(City)
    response['places'] = storage.count(Place)
    response['reviews'] = storage.count(Review)
    response['states'] = storage.count(State)
    response['users'] = storage.count(User)
    return jsonify(response)
