#!/usr/bin/python3
"""
    Script defines a route /status that
    returns a JSON response with the status "OK".
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status")
def get_status():
    """ get status """
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def number_of_each_obj():
    """ Retrive the number of each objects """
    number_of_obj = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "user": storage.count(User)
    }

    return jsonify(number_of_obj)
