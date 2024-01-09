#!/usr/bin/python3
"""eturns a JSON response
indicating the status is "OK".
"""
from flask import jsonify
from models import storage
from api.v1.views import app_views
from models.state import State
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    """Check the status of the route"""
    return jsonify({'status': 'OK'})


@app_views.route('/api/v1/nop', methods=['GET'], strict_slashes=False)
def nop():
    """Handles GET request to /api/v1/nop"""
    return jsonify({'error': 'Not found'}), 404


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def object_status():
    """Create an endpoint that retrieves the number of each object by type"""
    objects = {
        "amenities": 'Amenity',
        "cities": 'City',
        "places": 'Place',
        "reviews": 'Review',
        "states": 'State',
        "users": 'User'
    }
    object_counts = {
       key: storage.count(value) for key, value in objects.items()
   }
   return jsonify(object_counts)
