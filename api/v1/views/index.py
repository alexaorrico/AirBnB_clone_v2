#!/usr/bin/python3
"""New Funtion index"""
from api.v1.views import app_views
from flask import jsonify
from models.states import States
from models.city import City
from models.amenities import Amenity
from models.places import Places
from modes.review import Review
from models.users import Users


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def reoute_status():
    """first route
    Returns:
        json: json count number of instances
    """
    return jsonify({
        "status": "OK"
    }), 200


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def reoute_count():
    """objects by type """
    reoute_count = {
        'amenities': storage.count('Amenity'),
        'cities': storage.count('City'),
        'places': storage.count('Places'),
        'review': storage.count('Review'),
        'states': storage.count('States'),
        'users': storage.count('Users')
    }
    return jsonify(reoute_count)


if __name__ == '__main__':
    pass
