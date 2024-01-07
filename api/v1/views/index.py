#!/usr/bin/python3
"""index.py file"""

from api.v1.views import app_views
from flask import jsonify
from api.v1.views.states import *
from models import storage


ClassDict = {
    "states": "State",
    "cities": "City",
    "places": "Place",
    "amenities": "Amenity",
    "users": "User",
    "reviews": "Review"
}


@app_views.route('/status', methods=['GET'])
def status():
    """returns status of app"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def hbnbStatistics():
    """ Retrieves the number of objects by type """
    Dict = {}
    for key, val in ClassDict.items():
        Dict[key] = storage.count(val)
    return jsonify(Dict)
