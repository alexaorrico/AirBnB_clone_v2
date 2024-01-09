#!/usr/bin/python3

"""Creating index page"""
from api.v1.views import app_views
from flask import Flask, render_template, jsonify
from models import storage
from models.state import State
from models.amenity import Amenity
from models.place import Place
from models.city import City
from models.review import Review
from models.user import User


@app_views.route("/status", strict_slashes=False)
def index():
    """create a route /status on the object app_views that returns a JSON:"""
    status_dict = {"status": "OK"}
    return (jsonify(status_dict))


@app_views.route("/stats", strict_slashes=False)
def stats():
    """Returns counts for objects"""
    objs_dict = storage.all()
    count_dict = {}

    classes = [Amenity, City, Place, Review, State, User]

    for i in classes:
        count = storage.count(i)

        if count == 0:
            continue
        if i == Amenity:
            count_dict["amenities"] = count

        elif i == City:
            count_dict["cities"] = count

        elif i == Place:
            count_dict["places"] = count

        elif i == Review:
            count_dict["reviews"] = count

        elif i == State:
            count_dict["states"] = count

        elif i == User:
            count_dict["users"] = count

    return (jsonify(count_dict))
