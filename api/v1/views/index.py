#!/usr/bin/python3
"""this module handles status and stats routs"""

from flask import Flask, jsonify
from api.v1.views import app_views
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage
from sqlalchemy.sql.functions import user


@app_views.route('/status', methods=['GET'])
def status():
    """returns a JSON says the status of the API is OK"""
    return jsonify({"status": "OK"}), 200


@app_views.route('/stats')
def stats():
    """retrieves the number of each objects by type"""
    classes = {"amenities": Amenity, "cities": City, "places": Place,
               "reviews": Review, "states": State, "users": User}
    count_dict = {}
    for key, value in classes.items():
        count_dict[key] = storage.count(value)
    return jsonify(count_dict)
