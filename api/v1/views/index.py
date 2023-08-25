#!/usr/bin/python3
"""
Status route on app_views
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


@app_views.route('/status', strict_slashes=False)
def status():
    """Returns json status of route"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """"Retrieves dictionary obj count"""
    return {
        'amenities': storage.count(Amenity),
        'cities': storage.count(City),
        'place': storage.count(Place),
        'reviews': storage.count(Review),
        'states': storage.count(State),
        'users': storage.count(User)
    }