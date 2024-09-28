#!/usr/bin/python3
"""
    This Module contains the index
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


@app_views.route('/status', strict_slashes=False)
def status():
    """Return status of the application"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """An EndPoint that retrieves the number of each objects by type"""

    count = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }
    print(count)
    return jsonify(count)
