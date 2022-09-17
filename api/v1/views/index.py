#!/usr/bin/python3
"""Module index"""
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

@app_views.route('/status', strict_slashes=False)
def status():
    """Returns a JSON"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """retrieves the number of each objects by type"""
    classes = [Amenity, City, Place, Review, State, User]
    equal = ['amenities', 'cities', 'places', 'reviews', 'states', 'users']
    new_dict = {}

    for i in range(len(classes)):
        new_dict[equal[i]] = storage.count(classes[i])

    return jsonify(new_dict)