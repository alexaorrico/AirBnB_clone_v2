#!/usr/bin/python3
"""API index views modules"""
from models.city import City
from models.amenity import Amenity
from models.state import State
from models.place import Place
from models.review import Review
from models.user import Users
from models import storage
from api.v1.views import app_views
from flask import jsonify


@app_view.route('/status')
def status():
    """returns responses status in json format"""
    status = {"status": "OK"}
    return jsonify(status)


@app_view.route('/stats', strict_slashes=False)
def count():
    """Returns count of objects in the database"""

    models_available = {
        "User": "users",
        "Amenity": "amenities",
        "City": "cities",
        "Place": "places",
        "Review": "reviews",
        "State": "states",
    }

    model_objects = [Amenity, City, Place, Review, State, User]

    count = {}
    j = -1
    for cls in models_available.keys():
        j += 1
        count[models_available[cls]] = storage.count(model_objects[j])

    return jsonify(count)
