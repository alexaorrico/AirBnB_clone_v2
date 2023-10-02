#!/usr/bin/python3
""" The API index """
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


@app_views.route('/stats', strict_slashes=False)
def count():
    """
    returns a count of all database objects
    """

    models_list= {
        "User": "users",
        "Amenity": "amenities",
        "City": "cities",
        "Place": "places",
        "Review": "reviews",
        "State": "states",
    }
    mod_objs = [Amenity, City, Place, Review, State, User]

    count = {}
    i = -1
    for cls in models_list.keys():
        i += 1
        count[models_list[cls]] = storage.count(mod_objs[i])

    return jsonify(count)
