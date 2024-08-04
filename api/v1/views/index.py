#!/usr/bin/python3
'''
Create a route for status and stats
'''

from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.city import City
from models.amenity import Amenity
from models.user import User
from models.place import Place
from models.review import Review
from models.state import State

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Returns a JSON: {"status": "OK"}"""
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    return jsonify({
            "amenities": storage.count(Amenity),
            "cities": storage.count(City),
            "places": storage.count(Place),
            "reviews": storage.count(Review),
            "states": storage.count(State),
            "users": storage.count(User)})
