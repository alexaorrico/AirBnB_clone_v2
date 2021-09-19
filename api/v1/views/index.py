#!/usr/bin/python3
"""index"""
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', strict_slashes=False)
def status():
	return jsonify({"status": "OK"})

@app_views.route('/stats', strict_slashes=False)
def stats():
	return jsonify(
		{"amenities": "{}".format(storage.count(Amenity)),
		"cities": "{}".format(storage.count(City)),
		"places": "{}".format(storage.count(Place)),
		"reviews": "{}".format(storage.count(Review)),
		"states": "{}".format(storage.count(State)),
		"users": "{}".format(storage.count(User()))})
