#!/usr/bin/python3
""" Script to give the status of the files """
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/status')
def status():
    """status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def index():
    """ Count the whole information in the database
        with the newly added count()"""
    return jsonify({
            "amenities": storage.count(Amenity),
            "cities": storage.count(City),
            "places": storage.count(Place),
            "reviews": storage.count(Review),
            "states": storage.count(State),
            "users": storage.count(User)
        })
