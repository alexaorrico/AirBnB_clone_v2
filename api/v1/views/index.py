#!/usr/bin/python3
"""
This module defines the index view of the API.

Routes:
    /status: Returns the status of the API.
    /stats: Returns the number of objects by type.
"""

from api.v1.views import app_views, storage
from flask import jsonify

# Define a route to get the status of the API
@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_api_status():
    """
    Return the status of the API.

    Returns:
        A JSON response with a key "status" and value "OK".
    """
    return jsonify({"status": "OK"})

# Define a route to get the number of objects by type
@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_obj_counts():
    """
    Return the number of objects by type.

    Returns:
        A JSON response with keys representing object types and values representing
        the count of objects of each type.
    """
    class_counts = {}
    convert_dict = {
        'Amenity': 'amenities',
        'State': 'states',
        'City': 'cities',
        'User': 'users',
        'Place': 'places',
        'Review': 'reviews'
    }

    for obj_type, route_prefix in convert_dict.items():
        count = storage.count(obj_type)
        class_counts[route_prefix] = count

    return jsonify(class_counts)
