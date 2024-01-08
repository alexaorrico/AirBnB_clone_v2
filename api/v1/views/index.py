#!/usr/bin/python3
"""returns a JSON: "status": "OK"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status')
def status():
    """returns a JSON: "status": "OK" """
    response_data = {
            "status": "OK"
            }
    return jsonify(response_data)


@app_views.route('/stats')
def each_obj():
    """retrieves the number of each objects by type"""
    classes = {
            "Amenities": Amenity,
            "Cities": City,
            "Places": Place,
            "Reviews": Review,
            "States": State,
            "Users": User
            }
    each_obj = {}
    for key, value in classes.items():
        each_obj[key] = storage.count(value)

    return jsonify(each_obj)
