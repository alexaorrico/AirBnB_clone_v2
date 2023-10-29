#!/usr/bin/python3
"""
index of API
"""

from api.v1.views import app_views
from flask import jsonify, make_response
from models import storage
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.amenity import Amenity


@app_views.route('/status', methods=['GET'],  strict_slashes=False)
def status():
    """ Status of API """
    return make_response(jsonify({"status": "OK"}))


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def app_status():
    """ Retrieves the number of each objects by type """
    classes = [Amenity, City, Place, Review, State, User]
    names = ["amenities", "cities", "places", "reviews", "states", "users"]

    num_objs = {}
    for i in range(len(classes)):
        num_objs[names[i]] = storage.count(classes[i])

    return jsonify(num_objs)
