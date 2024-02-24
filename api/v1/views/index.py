#!/usr/bin/python3
"""
index.py
"""
from . import app_views
from flask import Flask, jsonify
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

all_classes = {"users": "User", "places": "Place", "states": "State",
               "cities": "City", "amenities": "Amenity",
               "reviews": "Review"}


@app_views.route('/status')
def status():
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    dictcount = {}
    for key, value in all_classes.items():
        dictcount[key] = storage.count(value)
    return jsonify(dictcount)
