#!/usr/bin/python3
""" Index.py """
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.engine.file_storage import FileStorage

classes = {"amenities": "Amenity", "cities": "City", "places": "Place",
           "reviews": "Review", "states": "State", "users": "User"}


@app_views.route('/status', methods=['GET'])
def code_status():
    """ Show status of the code"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def code_stats():
    """ Show statas about the classes
    counts the objects per class"""
    d = {p_cls: storage.count(r_cls) for p_cls, r_cls in classes.items()}
    return jsonify(d)
