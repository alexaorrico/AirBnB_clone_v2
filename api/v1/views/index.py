#!/usr/bin/python3
"""
this module contains flask app routes
    flask APP routes:
        /status:    print jsonify "status"
        /stats: print a count of objs storaged
"""

from api.v1.views import app_views
from flask import jsonify

# import all models
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status")
def status():
    "returns a serialized json data"
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stats():
    "returns a serialized count of all objs"
    return jsonify({
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    })
