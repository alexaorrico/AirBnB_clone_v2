#!/usr/bin/python3
from flask.helpers import make_response
from flask.json import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status", strict_slashes=False)
def get_status():
    """Return server status"""
    return jsonify(status="OK"), 200


@app_views.route("/stats", strict_slashes=False)
def get_stats():
    """Return stats for api"""
    amenities_count = storage.count(Amenity)
    cities_count = storage.count(City)
    places_count = storage.count(Place)
    reviews_count = storage.count(Review)
    states_count = storage.count(State)
    user_count = storage.count(User)
    return jsonify({"amenities": amenities_count, "cities": cities_count,
                    "places": places_count, "reviews": reviews_count,
                    "states": states_count, "users": user_count}), 200
