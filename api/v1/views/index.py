#!/usr/bin/python3
"""Define routes for blueprint    
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


#  Add views to app_views  using the route decorator
@app_views.route('/status')
def status():
    """ Returns status application """
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """ Method stast """
    return jsonify(
        {
            "amenities": storage.count("Amenity"),
            "cities": storage.count("City"),
            "places": storage.count("Place"),
            "reviews": storage.count("Review"),
            "states": storage.count("State"),
            "users": storage.count("User")
        }
    )
