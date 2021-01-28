#!/usr/bin/python3
"""imports app_views and routes /status on object app_view"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.state import State
from models.user import User
from models.place import Place
from models.city import City
from models.review import Review


@app_views.route("/status")
def app_status():
    ''' checks status of response '''
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def app_stats():
    ''' checks stats of response '''
    stats = {
            "amenities": storage.count(Amenity),
            "cities": storage.count(City),
            "places": storage.count(Place),
            "reviews": storage.count(Review),
            "states": storage.count(State),
            "users": storage.count(User)
            }
    return jsonify(stats)
