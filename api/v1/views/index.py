#!/usr/bin/python3
"""define routes of blueprint
"""

from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("/status", strict_slashes=False, methods=["GET"])
def status():
    return {
        "status": "OK",
    }


@app_views.route("/stats", strict_slashes=False, methods=["GET"])
def stats():
    amenities = storage.count(Amenity)
    cities = storage.count(City)
    places = storage.count(Place)
    reviews = storage.count(Review)
    states = storage.count(State)
    users = storage.count(User)
    return {
        "amenities": amenities,
        "cities": cities,
        "places": places,
        "reviews": reviews,
        "states": states,
        "users": users,
    }
