#!/usr/bin/python3
""" index file """

from api.v1.views import app_views
from models import storage
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.review import Review
from models.user import User


@app_views.route('/status')
def status():
    """ returns status """
    status = {"status": "OK"}
    return jsonify(status)


@app_views.route('/stats', strict_slashes=False)
def stats():
    """ returns number of objects by type """
    result = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }
    return jsonify(result)
