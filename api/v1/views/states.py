#!/usr/bin/python3
"""Handles RESTful API actions for State objects."""
from api.v1.views import app_views, storage
from flask import jsonify, abort


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieve list of all State objects."""
    states = []
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieve a specific State object by ID."""
    state = None
    if state is None:
        abort(404)
    return jsonify(state)

@app_views.route('/stats', methods=['GET'])
def stats():
    """
    Retrieves the number of each object by type
    """
    obj_dict = {
        "amenities": storage.count('Amenity'),
        "cities": storage.count('City'),
        "places": storage.count('Place'),
        "reviews": storage.count('Review'),
        "states": storage.count('State'),
        "users": storage.count('User')
    }
    return jsonify(obj_dict)
