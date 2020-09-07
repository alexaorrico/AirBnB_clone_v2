#!/usr/bin/python3
"""
Flask index file that returns the json status response
"""
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from flask import jsonify
from flask import request


@app_views.route('/status', methods=['GET'])
def status():
    """
    function for status route that returns the status
    """
    if request.method == 'GET':
        resp = {"status": "OK"}
        return jsonify(resp)


@app_views.route("/stats", strict_slashes=False)
def count_objects():
    """
    function for count each obj in each class
    """
    list_class = {"amenities": "Amenity",
                  "cities": "City",
                  "places": "Place",
                  "reviews": "Review",
                  "states": "State",
                  "users": "User"}
    dict_class = {}
    for item, val in list_class.items():
        dict_class[item] = storage.count(eval(val))
    return jsonify(dict_class)
