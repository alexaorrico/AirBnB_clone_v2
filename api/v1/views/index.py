#!/usr/bin/python3
"""Index module
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


@app_views.route('/status')
def get_status():
    """Get the API status
    """
    return jsonify({'status': 'OK'})


@app_views.route('/stats')
def get_stats():
    """GET the number of each objects by type
    """
    count_objs = {"amenities": storage.count(Amenity),
                  "cities": storage.count(City),
                  "places": storage.count(Place),
                  "reviews": storage.count(Review),
                  "states": storage.count(State),
                  "users": storage.count(User)}
    return jsonify(count_objs)
