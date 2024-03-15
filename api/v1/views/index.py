#!/usr/bin/python3
"""module that defines app_view func"""
from api.v1.views import app_views
from flask import Flask, jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"amenities": Amenity, "cities": City,
           "places": Place, "reviews": Review, "states": State, "users": User}


@app_views.route("/status")
def status():
    status = {
        "status": "OK"
    }
    return jsonify(status)


@app_views.route("/stats")
def stats():
    from models import storage
    d = {}
    for cls in classes:
        d.update({cls: storage.count(classes[cls])})
    return jsonify(d)
