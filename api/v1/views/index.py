#!/usr/bin/python3
""" Index view for the API """
from flask import jsonify
from api.v1.views import app_views
from models import storage

from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status')
def get_status():
    """Gets the status of the API"""
    return jsonify(status='OK')


@app_views.route('/stats')
def get_stats():
    """Gets number of objects for each type"""
    objects = {
        'amenitties': Amenity,
        'cities': City,
        'places': Place,
        'reviews': Review,
        'states': State,
        'users': User
    }
    for key, value in objects.items():
        objects[key] = storage.count(value)
    return jsonify(objects)
