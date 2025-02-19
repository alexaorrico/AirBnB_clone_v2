#!/usr/bin/python3
""" Method: Return JSON """
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review


@app_views.route("/status", strict_slashes=False)
def return_json():
    return (jsonify({"status": "OK"}))


@app_views.route("/stats", strict_slashes=False)
def get_stats():
    '''JSON Responses'''
    stats = {"states": State, "users": User,
             "amenities": Amenity, "cities": City,
             "places": Place, "reviews": Review}
    for key in stats:
        stats[key] = storage.count(stats[key])
    return jsonify(stats)
