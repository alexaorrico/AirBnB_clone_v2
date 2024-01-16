#!/usr/bin/python3
"""index.py file"""
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.review import Review
from models.user import User
from models.city import City
from models.state import State
from models.place import Place


@app_views.route('/status')
def index():
    """returns OK"""
    status = {"status": "OK"}
    return jsonify(status)


@app_views.route('/stats', strict_slashes=False)
def _count():
    '''returns stats'''
    stats = {"amenities": storage.count(Amenity),
             "cities": storage.count(City),
             "places": storage.count(Place),
             "reviews": storage.count(Review),
             "states": storage.count(State),
             "users": storage.count(User)}
    return jsonify(stats)
