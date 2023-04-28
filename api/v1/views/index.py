#!/usr/bin/python3
"""import app_views and creates the routes"""
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
def status():
    """returns a json"""
    return jsonify({"status": "OK"})

@app_views.route('/stats')
def object_count():
    """retrieves the number of each objects by type"""
    count = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
            }
    return jsonify(count)
