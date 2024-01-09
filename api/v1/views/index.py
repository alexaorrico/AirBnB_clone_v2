#!/usr/bin/python3

from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status', strict_slashes=False)
def status():
    """shows the status of a request"""
    status = {"status": "OK"}
    return jsonify(status)

@app_views.route('/stats',strict_slashes=False)
def stats():
    """no. of each objects"""
    resources = {
           "amenities": Amenity,
            "cities": City,
            "places": Place,
            "reviews": Review,
            "states": State,
            "users": User
            }
    stats = {}
    for key, value in (resources.items()):
        stats[key] = storage.count(value)
    return jsonify(stats)

#@app_views.route('/stats', methods=['GET'])
#def count_objs():
#    """ retrieve the number of each object by type """
#    return jsonify(amenities=storage.count("Amenity"),
#                   cities=storage.count("City"),
#                   places=storage.count("Place"),
#                   reviews=storage.count("Review"),
#                   states=storage.count("State"),
#                   users=storage.count("User"))
