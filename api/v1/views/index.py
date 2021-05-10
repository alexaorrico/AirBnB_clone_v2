#!/usr/bin/python3
"""
    This is the index page handler for Flask.
"""
from api.v1.views import app_views
from models import storage

classes = {"amenities": "Amenity",
           "cities": "City",
           "places": "Place",
           "reviews": "Review",
           "states": "State",
           "users": "User"}


@app_views.route('/status')
def status():
    """
        Flask route at /status.
        Displays the status of the API.
    """
    return {"status": "OK"}


@app_views.route('/stats')
def stats():
    """
        Flask route at /stats.
        Displays the number of each objects by type.
    """
    return {k: storage.count(v) for k, v in classes.items()}
