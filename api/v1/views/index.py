#!/usr/bin/python3
"""
    This module handles some routing options for the flask app

"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status')
def get_status():
    """ Tests the route status returning a basic JSON query """
    dic = {'status': 'OK'}
    return jsonify(dic)


@app_views.route('/stats')
def get_stats():
    """ Gets the count of all objects created """
    dic = {
        'amenities': storage.count(Amenity),
        'cities': storage.count(City),
        'places': storage.count(Place),
        'reviews': storage.count(Review),
        'states': storage.count(State),
        'users': storage.count(User)
    }
    return jsonify(dic)
