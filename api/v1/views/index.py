#!/usr/bin/python3
""" index module"""

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status", strict_slashes=False, methods=["GET"])
def status():
    return {
        "status": "OK"
    }


@app_views.route("/stats", strict_slashes=False, methods=["GET"])
def stats():
    amenity = storage.count(Amenity)
    city = storage.count(City)
    place = storage.count(Place)
    review = storage.count(Review)
    state = storage.count(State)
    user = storage.count(User)
    return {
        "amenities": amenity,
        "cities": city,
        "places": place,
        "reviews": review,
        "states": state,
        "users": user
    }
