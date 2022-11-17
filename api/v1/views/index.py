#!/usr/bin/python3
"""index file, where everything start and end"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status')
def status():
    """Return that the status is ok in json format"""
    stat = {"status": "OK"}
    return jsonify(stat)


@app_views.route('/stats')
def countstorage():
    """count all element inside each class and return
       class and number of objet inside in json format"""
    classes = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }
    return classes
