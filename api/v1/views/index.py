#!/usr/bin/python3
""" route for defining JSON """
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'])
def index():
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def count_objs():
    """ retrieve the number of each object by type """
    return jsonify(amenities=storage.count("Amenity"),
                   cities=storage.count("City"),
                   places=storage.count("Place"),
                   reviews=storage.count("Review"),
                   states=storage.count("State"),
                   users=storage.count("User"))
