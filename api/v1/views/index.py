#!/usr/bin/python3
""" Gives the status of the api """
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def app_status():
    """ Returns the status of the app in json format """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def obj_stats():
    """ Returns the number of each object by type """
    m_classes = {"amenities": Amenity, "cities": City, "places": Place,
                 "reviews": Review, "states": State, "users": User}
    count = {}
    for key, val in m_classes.items():
        count[key] = storage.count(val)
    return jsonify(count)
