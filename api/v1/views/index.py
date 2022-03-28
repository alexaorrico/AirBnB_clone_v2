#!/usr/bin/python3
"""index file for api"""
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

@app_views.route('/status')
def status(text="is_cool"):
    """returns JSON status"""
    return jsonify({"status": "OK"})

@app_views.route('/stats')
def count_objects(text="is_cool"):
    """returns count of objects by type"""
    count = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User),
        "all": storage.count()
        }
    return jsonify(count)
