#!/usr/bin/python3
"""index creates route for status"""


from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status')
def get_status():
    """returns status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def get_count():
    """gets count of each object by type"""
    # crate dict to hold count of each object type
    obj_count = {}
    # count each object type
    obj_count["amenities"] = storage.count(Amenity)
    obj_count["cities"] = storage.count(City)
    obj_count["places"] = storage.count(Place)
    obj_count["reviews"] = storage.count(Review)
    obj_count["states"] = storage.count(State)
    obj_count["users"] = storage.count(User)
    return jsonify(obj_count)
