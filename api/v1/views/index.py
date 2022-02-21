#!/usr/bin/python3
"""API index views module"""
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage
from api.v1.views import app_views
from models import storage
from flask import jsonify

mod_objs = [Amenity, City, Place, Review, State, User]

@app_views.route('/status')
def status():
    """
    Returns json response as the status

    Returns:
        JSON: json object
    """
    status = {
        "status": "OK"
    }
    return jsonify(status)


@app_views.route('/stats')
def count():
    """[summary]
    """

    models_avail = {
        "User": "users",
        "Amenity": "amenities", 
        "City": "cities",
        "Place": "places", 
        "Review": "reviews",
        "State": "states",
    }

    count = {}
    i = 0
    for cls in models_avail.keys():
        count[models_avail[cls]] = storage.count(mod_objs[i])
        i += 1

    return jsonify(count)
