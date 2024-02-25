#!/usr/bin/python3
"""return JSON status on object app_views"""

from api.v1.views import app_views
from models import storage


@app_views.route('/status')
def status():
    """ Returns status message in JSON
    """
    return ({"status": "OK"})


@app_views.route('/stats')
def stats():
    """ Returns stats message in JSON
    """
    amens = storage.count("Amenity")
    cities = storage.count("City")
    places = storage.count("Place")
    reviews = storage.count("Review")
    states = storage.count("State")
    users = storage.count("User")

    return ({"amenities": amens,
             "cities": cities,
             "places": places,
             "reviews": reviews,
             "states": states,
             "users": users})
