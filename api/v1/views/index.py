#!/usr/bin/python3
"""First route to display a json object"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


tables = {"amenities": Amenity, "cities": City,
          "places": Place, "reviews": Review, "states": State, "users": User}


@app_views.route('/status')
def status():
    return jsonify(status="OK")


@app_views.route('/stats')
def stats():
    counts = {}
    for key, val in tables.items():
        counts[key] = storage.count(val)
    return jsonify(**counts)
