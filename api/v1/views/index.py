#!/usr/bin/python3
"""Creation of API endpoints"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
# Importing classes from models directory
from models.amenity import Amenity
from models.city import City
from models.user import User
from models.review import Review
from models.place import Place
from models.state import State


@app_views.route('/status', strict_slashes=False)
def status_api():
    """Returning API status"""
    return (jsonify({"status": "OK"}))


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats_api():
    """Endpoint that retrieves the number of each objects by type"""
    return (jsonify({"amenities": storage.count(Amenity),
                     "cities": storage.count(City),
                     "places": storage.count(Place),
                     "reviews": storage.count(Review),
                     "states": storage.count(State),
                     "users": storage.count(User)}))
