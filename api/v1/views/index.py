#!/usr/bin/python3
"""Return the status of your API:"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.amenity import Amenity


@app_views.route("/status")
def status():
    """Returns the server status."""
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stats():
    """Returns the server status."""
    states_count = storage.count(State)
    cities_count = storage.count(City)
    places_count = storage.count(Place)
    reviews_count = storage.count(Review)
    users_count = storage.count(User)
    amenities_count = storage.count(Amenity)

    return jsonify({
        "amenities": amenities_count,
        "cities": cities_count,
        "places": places_count,
        "reviews": reviews_count,
        "states": states_count,
        "users": users_count
    })
