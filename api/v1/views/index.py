#!/usr/bin/python3
"""Status of your API"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status")
def function_hola():
    """Function status return OK"""
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def function():
    """Function stats"""
    clases = {
         "amenities": Amenity,
         "cities": City,
         "places": Place,
         "reviews": Review,
         "states": State,
         "users": User}
    dic = {}
    for key, cls in clases.items():
        x = storage.count(cls)
        dic[key] = x
    return jsonify(dic)
