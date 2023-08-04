#!/usr/bin/python3
"""Index view for the web service API"""
from flask import jsonify, make_response
from api.v1.views import app_views  # Blueprint object
from models import storage
from models.review import Review
from models.state import State
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place


@app_views.route('/status')
def status():
    """Return API status"""
    return jsonify(status='OK')


@app_views.route('/stats')
def stats(cls):
    """Return number of objects by type"""

    objects = {
        'states': State,
        'users': User,
        'amenities': Amenity,
        'cities': City,
        'places': Place,
        'reviews': Review
    }

    for key, value in objects.items():
        # count objects by type from storage
        objects[key] = storage.count(value)
    return jsonify(objects)
