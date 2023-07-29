#!/usr/bin/python3
"""Flask with general routes"""
from api.v1.views import app_views
from flask import jsonify
import json
from models import storage
from models.amenity import Amenity
from models.city import City
from models.state import State
from models.place import Place
from models.user import User
from models.review import Review

@app_views.route("/status", methods=['GET'])
def status():
    """Returns a JSON status"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=['GET'])
def stats():
    """
    Retrieves the number of each objects by type
    """
    classes = {
        "amenities": storage.count(Amenity),
        "City": storage.count(City),
        "Place": storage.count(Place),
        "Review": storage.count(Review),
        "State": storage.count(State),
        "User": storage.count(User)
    }
    objs = json.dumps(classes, indent=2)
    return objs
