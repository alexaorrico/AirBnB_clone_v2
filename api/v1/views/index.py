#!/usr/bin/python3
""" route for defining JSON """
from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.state import State
from models.user import User
from models.review import Review
from models.place import Place
from models import storage


@app_views.route('/status', strict_slashes=False)
def index():
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def count_objs():
    """ retrieve the number of each object by type """
    classes = [Amenity, City, Place, Review, State, User]
    names = ["amenities", "cities", "places", "reviews", "states", "users"]
    counts = {}
    for num in range(len(classes)):
        counts[names[num]] = storage.count(classes[num])
    return jsonify(counts)
