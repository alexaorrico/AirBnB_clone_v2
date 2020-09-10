#!/usr/bin/python3
""" Module to retrives an object """
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
    """
    Return status ok
    Returns:
        json: status
    """
    return jsonify({"status": "OK"})

@app_views.route('/stats')
def show_stats():
    """
    Returns:
        json: number of objects
    """
    data = {
        'amenities': storage.count(Amenity),
        'cities': storage.count(City),
        'places': storage.count(Place),
        'reviews': storage.count(Review),
        'states': storage.count(State),
        'users': storage.count(User)
    }
    return jsonify(data)