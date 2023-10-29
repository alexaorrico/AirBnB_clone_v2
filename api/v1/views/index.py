#!/usr/bin/python3
"""API Index Module

This module defines routes for the API status and statistics endpoints.
"""

from api.v1.views import app_views

@app_views.route("/status", methods=["GET"])
def status():
    """API Status Endpoint

    Returns:
        dict: A dictionary with the status message.
    """
    return {"status": "OK"}

@app_views.route("/stats", methods=["GET"])
def stats():
    """API Statistics Endpoint

    Computes and returns the count of objects for each model class in the storage.

    Returns:
        dict: A dictionary containing counts of different object types.
    """
    from models import storage
    from models.amenity import Amenity
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models.user import User

    # Count objects for each model class
    count = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User),
    }

    return count
