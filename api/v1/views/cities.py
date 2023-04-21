#!/usr/bin/python3
"""Handles RESTful API actions for City objects."""
from api.v1.views import app_views
from flask import jsonify, abort


@app_views.route('/cities', methods=['GET'], strict_slashes=False)
def get_cities():
    """Retrieve list of all City objects."""
    cities = []  # replace with code to retrieve list of cities from storage
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Retrieve a specific City object by ID."""
    city = None  # replace with code to retrieve city from storage by ID
    if city is None:
        abort(404)
    return jsonify(city)
