#!/usr/bin/python3
""" this area is for description"""

from api.v1.views import app_views
from flask import make_response, jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def api_resp():
    """ return api response status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_data():
    """ retrieves the number of each objects"""
    cls = [Amenity, City, Place, Review, State, User]
    loc = ["amenities", "cities", "places", "reviews", "states", "users"]
    dict_struc = {}
    for i in range(len(cls)):
        dict_struc[loc[i]] = storage.count(cls[i])

    return jsonify(dict_struc)
