#!/usr/bin/python3
"""Index"""


from models import storage
from flask import jsonify
from api.v1.views import app_views
from models.amenity import Amenity
from models.city import City
from models.state import State
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ API status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def object_count():
    """endpoint that retrieves the number of each objects by type"""
    classes = [Amenity, City, State, Place, User, Review]
    titles = ['amenities', 'cities', 'states', 'places', 'users', 'reviews']

    obj_count = {}
    for i in range(len(classes)):
        obj_count[titles[i]] = storage.count(classes[i])

    return jsonify(obj_count)
