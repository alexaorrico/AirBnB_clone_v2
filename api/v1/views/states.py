#!/usr/bin/python3
"""
Create a new view for State objects - handles all default RESTful API actions
"""

from flask import Flask, jsonify, abort, request
from models.state import State
from api.v1.views import app_views
from models import storage


@app_views.route("/states")
def get_all_states():
    """
    Retrieves the list of all State
    """
    states = storage.all(State).values()
    state_list = [state.to_dict() for state in states]
    return jsonify(state_list)


@app_views.route("/states/<state_id>")
def some_state(state_id):
    """
    Retrieves a state object
    """
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route("/states/<state_id>")
def delete_state(state_id):
    """
    Delete state object
    """
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/states")
def create_state():
    """
    Create a state object
    """
    if not request.get_json():
        abort(400, "Not a JSON")

    # Get the JSON data from the request
    kwargs = request.get_json()
    if "name" not in kwargs:
        abort(400, "Missing name")

    # Create a new state object with the json data
    state = State(**kwargs)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>')
def update_state(state_id):
    """
    Updates a State object.
    """
    # Get the State object with the given ID from the storage
    state = storage.get(State, state_id)
    if state:
        if not request.get_json():
            abort(400, 'Not a JSON')

        # Get the JSON data from the request
        data = request.get_json()
        ignore_keys = ['id', 'created_at', 'updated_at']
        # Update the attributes of the State object with the JSON data
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(state, key, value)

        # Save the updated State object to the storage
        state.save()
        return jsonify(state.to_dict()), 200
    else:
        abort(404)


@app_views.errorhandler(404)
def not_found(error):
    """
    Raises a 404 error.
    """
    # Return a JSON response for 404 error
    response = {'error': 'Not found'}
    return jsonify(response), 404


@app_views.errorhandler(400)
def bad_request(error):
    """
    Returns a Bad Request message for illegal requests to the API.
    """
    # Return a JSON response for 400 error
    response = {'error': 'Bad Request'}
    return jsonify(response), 400
