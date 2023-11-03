#!/usr/bin/python3
"""for the following files"""
from flask import jsonify
from models import storage

from api.v1.views import app_views
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {
    "amenities": Amenity,
    "cities": City,
    "places": Place,
    "reviews": Review,
    "states": State,
    "users": User,
}


@app_views.route("/status", methods=["GET"], strict_slashes=False)
def status():
    """return the status of the application"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=["GET"], strict_slashes=False)
def stats():
    """return the stats of the application"""
    new_d = {key: storage.count(val) for key, val in classes.items()}

    return jsonify(new_d)
