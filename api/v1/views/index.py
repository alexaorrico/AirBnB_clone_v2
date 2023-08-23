#!/usr/bin/python3
"""run script"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.amenity import Amenity


@app_views.route("/status")
def status():
    """returns a json representation of status"""
    return jsonify({"status": "OK"})


@app_views.route('/api/v1/stats', methods=['GET'])
def stats():
    """return a json representation of the objects counted"""
    objs = {
      "amenities": storage.count(Amenity),
      "cities": storage.count(City),
      "places": storage.count(Place),
      "reviews": storage.count(Review),
      "states": storage.count(State),
      "users": storage.count(User)
    }
    return jsonify(objs)