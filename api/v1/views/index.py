#!/usr/bin/python3
"""
Index
"""
from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.state import State
from models.review import Review
from models.place import Place
from models.user import User
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    """
    Returns:
        Status of API
    """
    if request.method == 'GET':
        response = {"status": "OK"}
        return jsonify


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def number_objs():
    """

    """
    classes = [Amenity, City, State, Review, Place, User]
    names = ["amenities", "cities", "places", "reviews", "states", "users"]

    objs = {}
    for index in range(len(classes)):
        objs[names[index]] = storage.count(classes[index])

    return jsonify(objs)
