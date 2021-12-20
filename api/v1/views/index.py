#!/usr/bin/python3
"""
index module
"""

from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status", methods=["GET"])
def status():
    """
    status of api
    """
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=["GET"])
def stats():
    """Retrieves the number of each object by type"""
    dic = {
            'amenities': storage.count('Amenity'),
            'cities': storage.count('City'),
            'places': storage.count('Place'),
            'reviews': storage.count('Review'),
            'states': storage.count('State'),
            'users': storage.count('User')
          }
    return jsonify(dic)
