#!/usr/bin/python3
""" holds class State"""

from flask import Blueprint, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def get_post_states():
    """Handles GET and POST requests"""
    if request.method == 'GET':
        # Retrieve all states and return in JSON format
        return jsonify([
            state.to_dict() for state in storage.all('State').values()
            ])
    elif request.method == 'POST':
        # Create a new state based on POST data in JSON format
        request_data = request.get_json()
        if request_data is None or not isinstance(request_data, dict):
            return jsonify({'error': 'Invalid JSON'}), 400
        elif 'name' not in request_data:
            return jsonify({'error': 'Missing name parameter'}), 400
        new_state = State(**request_data)
        new_state.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route(
        '/states/<string:state_id>',
        methods=['GET', 'PUT', 'DELETE'],
        strict_slashes=False
        )
def get_put_delete_state(state_id):
    """Handles GET (retrieve), PUT (update), and DELETE (remove)"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)  # Return 404 if state with given ID doesn't exist
    elif request.method == 'GET':
        # Return details of the state in JSON format
        return jsonify(state.to_dict())
    elif request.method == 'DELETE':
        storage.delete(state)  # Delete the specified state
        storage.save()  # Save changes
        return jsonify({}), 200  # Return empty JSON
    elif request.method == 'PUT':
        # Update attributes of the state based on PUT data
        put_data = request.get_json()
        if put_data is None or not isinstance(put_data, dict):
            return jsonify({'error': 'Invalid JSON'}), 400
        for key, value in put_data.items():
            if key != 'id' and key != 'created_at' and key != 'updated_at':
                setattr(state, key, value)
        storage.save()  # Save changes
        return jsonify(state.to_dict()), 200  # Return update
