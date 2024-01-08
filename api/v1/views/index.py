#!/usr/bin/python3
"""index"""


from models.amenity import Amenity
from models.state import State
from models.place import Place
from api.v1.views import app_views
from flask import jsonify
from models import *
from models.city import City
from models.review import Review
from models.user import User


@app_views.route('/status')
def status():
    """return status"""
    stat = {"status": "OK"}
# json_response_stat = jsonify(stat)
    return jsonify(stat), 200


@app_views.route('/stats')
def stats():
    """retrieves the number of each objects by type"""
    obj_count = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }

    return jsonify(obj_count), 200
