#!/usr/bin/python3
""" Module that represents index """
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def status():
    """ Status code """
    return jsonify({'status': 'OK'})


@app_views.route('/stats', methods=['GET'])
def stats():
    """ Endpoint that retrieves the number of each objects by type """
    classes = [Amenity, City, Place, Review, State, User]
    variables = ["amenities", "cities", "places", "reviews", "states", "users"]
    stats_dict = {}
    for i in range(len(classes)):
        stats_dict[variables[i]] = storage.count(classes[i])

    return jsonify(stats_dict)
