#!/usr/bin/python3
"""Status of your API"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status")
def function_hola():
    """function"""
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def function():
    """function"""

    clases = ["Amenity", "City", "Place", "Review", "State", "User"]
    dic = {}
    for cls in clases:
        x = storage.count(eval(cls))
        dic[cls] = x
    return jsonify(dic)
