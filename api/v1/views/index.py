#!/usr/bin/python3
"""index file"""
import json
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.engine.db_storage import classes


@app_views.route("/status")
def return_status():
    """returns status of the api"""
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def return_count():
    """counts and returns the number of objects"""
    count_dict = {}
    count_dict["amenities"] = storage.count(classes["Amenity"])
    count_dict["cities"] = storage.count(classes["City"])
    count_dict["places"] = storage.count(classes["Place"])
    count_dict["reviews"] = storage.count(classes["Review"])
    count_dict["states"] = storage.count(classes["State"])
    count_dict["users"] = storage.count(classes["User"])
    return(jsonify(count_dict))
