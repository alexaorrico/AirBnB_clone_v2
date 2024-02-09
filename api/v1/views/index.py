#!/usr/bin/python3
'''index for the api app
This module defines routes related to the status and statistics of the API.
'''
from api.v1.views import app_views
from flask import jsonify, Flask
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', strict_slashes=False)
def status():
    '''Returns the status of the API in JSON format.

    Returns:
        A JSON response containing the API status.
    '''
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stat():
    '''Returns statistics about the number of each
    object type in the database.

    Returns:
        A JSON response containing the counts of different object types.
    '''
    return jsonify({"amenities": storage.count(Amenity),
                    "cities": storage.count(City),
                    "places": storage.count(Place),
                    "reviews": storage.count(Review),
                    "states": storage.count(State),
                    "users": storage.count(User)})
