#!/usr/bin/python3

""" View module for State objects that handles all default RESTFul API actions
"""

# Import necessary modules
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State


# Define a route for handling GET and POST requests for all states
@app_views.route('/states', strict_slashes=False, methods=['GET', 'POST'])
def all_states():
    """Handles GET and POST requests for all State objects.
    """
    if request.method == 'GET':
        # Return a JSON representation of all State objects
        return jsonify([
            state.to_dict() for state in storage.all(State).values()])

    elif request.method == 'POST':
        # Handle POST request to create a new State object
        data = request.get_json()
        if not data:
            return jsonify({"error": "Not a JSON"}), 400
        if 'name' not in data:
            return jsonify({"error": "Missing name"}), 400

        # Create a new State instance and save it
        new_state = State(**data)
        new_state.save()
        return jsonify(new_state.to_dict()), 201


# Define a route for handling GET, PUT, and DELETE requests
# for a specific state
@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'])
def state_by_id(state_id):
    """Handles GET, DELETE, and PUT requests for a specific State object.
    """
    # Retrieve the State object with the given ID
    state = storage.get(State, state_id)
    if state is None:
        # Return a 404 error if the State object is not found
        abort(404)

    if request.method == 'GET':
        # Return a JSON representation of the specific State object
        return jsonify(state.to_dict())

    elif request.method == 'DELETE':
        # Handle DELETE request to delete the specific State object
        storage.delete(state)
        storage.save()
        return jsonify({}), 200

    elif request.method == 'PUT':
        # Handle PUT request to update the specific State object
        data = request.get_json()
        if not data:
            return jsonify({"error": "Not a JSON"}), 400

        # Update the State object's attributes based on the request data
        ignore_keys = ['id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(state, key, value)

        # Save the updated State object
        storage.save()
        return jsonify(state.to_dict()), 200
