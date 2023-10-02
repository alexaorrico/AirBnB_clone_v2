#!/usr/bin/python3
"""index for connecting to APIs"""
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify
from models import storage

"""dictionary to map endpoint names to their object types"""
endpoint_to_object_type = {
    "amenities": "Amenity",
    "cities": "City",
    "places": "Place",
    "reviews": "Review",
    "states": "State",
    "users": "User"
}

"""Define a route for the /status endpoint"""
@app_views.route('/status', strict_slashes=False)
def hbnb_status():
    """Return Status"""
    return jsonify({"status": "OK"})

"""Define a route for the /stats endpoint"""
@app_views.route('/stats', strict_slashes=False)
def hbnb_stats():
    """Return Stats"""
    stats_dict = {}
    
    """Loop through the endpoint-to-object-type mapping"""
    for endpoint, object_type in endpoint_to_object_type.items():
        """Use the storage.count method to get 
        the count of objects for each type"""
        stats_dict[endpoint] = storage.count(object_type)
    
    return jsonify(stats_dict)

if __name__ == "__main__":
    pass
