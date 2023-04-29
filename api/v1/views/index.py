#!/usr/bin/python3
''' index and status view for the API'''
from flask import jsonify
from models import storage
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status')
def get_api_status():
    '''Gets the status of the api
    '''
    # return jsonify(status='OK')
    return jsonify({'status': 'OK'})


@app_views.route('/stats')
def get_api_stats():
    """gets the number of each objects"""

    stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }

    return jsonify(stats)
