#!/usr/bin/python3
"""Index file for views module"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


classes = {"amenities": Amenity, "cities": City,
           "places": Place, "reviews": Review, "states": State, "users": User}


@app_views.route('/status')
def status():
    """Status route of API v1"""
    return jsonify({"status": "OK"}), 200


@app_views.route('/stats')
def stats():
    """Stats route of API v1 """
    d = {}
    for cls in classes.items():
        d[cls[0]] = storage.count(cls[1])
    return jsonify(d)
