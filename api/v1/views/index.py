#!/usr/bin/python3
"""index.py that returns a JSON"""

from api.v1.views import app_views, jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

@app_views.route("/status")
def status():
    """ status method"""
    data = {
        'status': 'OK'
    }
    return (jsonify(data))


@app_views.route('/stats')
def stats():

    data = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User),
    }

    return jsonify(data)
