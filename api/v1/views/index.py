#!/usr/bin/python3
"""
Module defining routes for api
"""
from api.v1.views import app_views
from flask import jsonify
from models.state import State
from models.amenity import Amenity
from models.city import City
from models.review import Review
from models.user import User
from models import storage
from models.place import Place


@app_views.route('/status')
def status():
    """ Display a json of the status """
    return jsonify(status="OK")


@app_views.route('/stats')
def stats():
    """ Retrieves the number of each objects by type """
    objects = {
        'amenities': storage.count(Amenity),
        'cities': storage.count(City),
        'places': storage.count(Place),
        'reviews': storage.count(Review),
        'states': storage.count(State),
        'users': storage.count(User)
    }
    return jsonify(objects)
