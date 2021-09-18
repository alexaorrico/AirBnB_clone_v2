#!/uar/bin/python3
"""Is the Status of your API dile"""
from api.v1.views import app_views
from flask import jsonify

from models import storage
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.state import State, City
from models.user import User


@app_views.route("/status", methods=["GET"])
def status():
    """"Function that return a JSON dictionary"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=["GET"])
def number_each_object():
    """"Function that returns the number of each objects by type"""
    objects = {}
    objects["amenities"] = storage.count(Amenity)
    objects["cities"] = storage.count(City)
    objects["places"] = storage.count(Place)
    objects["reviews"] = storage.count(Review)
    objects["states"] = storage.count(State)
    objects["users"] = storage.count(User)

    return jsonify(objects)
