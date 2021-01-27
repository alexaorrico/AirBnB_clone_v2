#!/usr/bin/python3
"""route /status on the object app_views that returns a JSON"""
from api.v1.views import app_views
from flask import jsonify
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.user import User
from models.place import Place
from models.review import Review
from models import storage
import itertools


@app_views.route("/status")
def status():
    """returns a JSON"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def stats():
    """retrieves the number of each objects by type"""
    clases = [Amenity, City, Place, Review, State, User]
    name_class = [
            "amenities",
            "cities",
            "places",
            "reviews",
            "states",
            "users"]
    dic = {}
    for name, clase in zip(name_class, clases):
        dic[name] = storage.count(clase)
    return jsonify(dic)
