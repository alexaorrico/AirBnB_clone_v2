#!/usr/bin/python3
"""The home web Page"""

from api.v1.views import app_views
from models import storage
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status")
def status():
    """Return the a json dict status"""
    return jsonify({'status': 'OK'})


@app_views.route("/stats")
def stats():
    """return the numeber of rows in a table"""
    tables = {}
    tables = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }
    return jsonify(tables)
