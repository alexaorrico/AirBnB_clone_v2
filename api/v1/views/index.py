#!/usr/bin/python3
"""Index file"""

from flask import jsonify
from models import storage
from api.v1.views import app_views
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.amenity import Amenity


@app_views.route('/status', methods=['GET'])
def status():
    """Returns status of app"""
    return jsonify({'status': 'OK'})

@app_views.route('/stats', methods=['GET'])
def stat():
    """Returns statistics of objects"""
    sts_dict = {
                "amenities": storage.count(Amenity), 
                "cities": storage.count(City), 
                "places": storage.count(Place), 
                "reviews": storage.count(Review), 
                "states": storage.count(State), 
                "users": storage.count(User)
                }
    return jsonify(sts_dict)