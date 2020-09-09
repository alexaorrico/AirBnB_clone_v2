#!/usr/bin/python3
"""Index of the application"""
from api.v1.views import app_views
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def Index():
    """Function index"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def number_objects():
    """counts the number of objects for each model"""

    classes = {
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review,
        "states": State,
        "users": User}
    dictionary = {}
    for key, cl in classes.items():
        numb = storage.count(cl)
        dictionary[key] = numb
    return jsonify(dictionary)
