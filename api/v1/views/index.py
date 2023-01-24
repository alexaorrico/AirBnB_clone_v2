#!/usr/bin/python3
"""App Views API"""
from models import storage
from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

@app_views.route("/status")
def status():
    """Return status of the API server"""
    return jsonify({"status": "OK"})

@app_views.route("/stats")
def stats():
    """Return the stats of the data"""
    amenities_cnt = storage.count(Amenity)
    cities_cnt = storage.count(City)
    places_cnt = storage.count(Place)
    reviews_cnt = storage.count(Review)
    states_cnt = storage.count(State)
    users_cnt = storage.count(User)

    stats = {
        "amenities": amenities_cnt, 
        "cities": cities_cnt, 
        "places": places_cnt, 
        "reviews": reviews_cnt, 
        "states": states_cnt, 
        "users": users_cnt,
    }

    return jsonify(stats)