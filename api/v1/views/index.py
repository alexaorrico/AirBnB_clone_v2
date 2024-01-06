#!/usr/bin/python3
"""imports app_views and creates a route /status"""

from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json


@app_views.route("/status")
def status_returns():
    """returns a json file"""
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def no_of_objects():
    """returns the number of objects"""
    data = {"amenities": storage.count(Amenity),
            "cities": storage.count(City),
            "Places": storage.count(Place),
            "reviews": storage.count(Review),
            "states": storage.count(State),
            "users": storage.count(User)
            }
    returned_data = json.dumps(data)
    return (returned_data)
