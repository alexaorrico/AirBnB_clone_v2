#!/usr/bin/python3
"""Handles RESTful API actions for Place objects."""
from api.v1.views import app_views
from flask import jsonify, abort


@app_views.route('/places', methods=['GET'], strict_slashes=False)
def get_places():
    """Retrieve list of all Place objects."""
    places = []
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieve a specific Place object by ID."""
    place = None
    if place is None:
        abort(404)
    return jsonify(place)
