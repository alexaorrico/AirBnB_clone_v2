#!/usr/bin/python3
"""Module that retreives JSON responses"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.user import User
from models.place import Place


@app_views.route('/status')
def status():
    """Retreive the status of the app"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def number_objs_type():
    """Retreive the number of instances grouped by class type"""
    classes = [State, City, User, Amenity, Place, Review]
    names = ['states', 'cities', 'users', 'amenities', 'places', 'reviews']
    response = {}
    for c, n in zip(classes, names):
        response[n] = storage.count(c)
    return jsonify(response)
