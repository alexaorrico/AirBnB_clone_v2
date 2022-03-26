#!/usr/bin/python3
"""This module houses the index for the api"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', strict_slashes=False, methods=['GET'])
def status():
    """ returns the status 'ok' if api is running """
    return jsonify({'status': 'OK'})


@app_views.route('/stats', strict_slashes=False, methods=['GET'])
def stats():
    """ returns the number of classes of each type """
    classes = [State, City, Amenity, Review, Place, User]
    classnames = [
        "states", "cities", "amenities", "reviews", "places", "users"]
    class_count = {}
    for x in range(len(classes)):
        class_count[classnames[x]] = storage.count(classes[x])
    return jsonify(class_count)
