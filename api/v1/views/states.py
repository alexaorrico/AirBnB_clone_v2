#!/usr/bin/python3
"""
    Handles API functions for State objects
"""

from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def get_states():
    """
        Returns all states
    """
    if request.method == 'GET':
        states_list = []
        for state in storage.all(State).values():
            states_list.append(state.to_dict())
        return jsonify(states_list)
    if request.method == 'POST':
        info = request.get_json(silent=True)
        if not info:
            abort(400, description='Not a JSON')
        if 'name' not in info:
            abort(400, description='Missing name')
        state = State(**info)
        state.save()
        return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def handle_a_state(state_id):
    """
        Returns a state specified by id
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(state.to_dict())
    if request.method == 'DELETE':
        for city in state.cities:
            for place in city.places:
                for review in place.reviews:
                    storage.delete(review)
                storage.delete(place)
            storage.delete(city)
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        info = request.get_json(silent=True)
        if not info:
            abort(400, 'Not a JSON')
        for key, value in info.items():
            if key in ['id', 'created_at', 'updated_at']:
                pass
            else:
                setattr(state, key, value)
        state.save()
        return jsonify(state.to_dict()), 200
