#!/usr/bin/python3
"""
This module defines API routes for the project.

Routes:
    /status: Returns the status of the API.
    /stats: Returns the number of records in the database for each model.
"""


from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


@app_views.route('/status', strict_slashes=False)
def index():
    """
     Return status of API.
     Used to check if user is allowed to access API

     @return jsonified version of status
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def count():
    """
     Count how many records exist in the database.
     This is useful for determining if a query is valid or not.

     @return 200 if everything worked 400 if something went wrong with the
    """

    return jsonify({
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "state": storage.count(State),
        "users": storage.count(User),
    })
