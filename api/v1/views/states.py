#!/usr/bin/python3
"""Objects that handle all default RestFul API actions for States"""

# Import necessary modules and classes
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request

# Route to retrieve the list of all State objects
@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects"""
    # Retrieve all State objects from the storage
    all_states = storage.all(State).values()

    # Convert State objects to dictionaries
    list_states = [state.to_dict() for state in all_states]

    # Return the list of State dictionaries as JSON
    return jsonify(list_states)

# Route to retrieve a specific State by ID
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieves a specific State"""
    # Get the State object with the specified ID from the storage
    state = storage.get(State, state_id)

    # If State not found, return 404 Not Found
    if not state:
        abort(404)

    # Return the State dictionary as JSON
    return jsonify(state.to_dict())

# Route to delete a specific State by ID
@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Deletes a State Object"""
    # Get the State object with the specified ID from the storage
    state = storage.get(State, state_id)

    # If State not found, return 404 Not Found
    if not state:
        abort(404)

    # Delete the State object and save changes to storage
    storage.delete(state)
    storage.save()

    # Return an empty JSON response with status 200 OK
    return make_response(jsonify({}), 200)

# Route to create a new State
@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """Creates a State"""
    # Check if the request contains JSON data
    if not request.get_json():
        abort(400, description="Not a JSON")

    # Check if the 'name' key is present in the JSON data
    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    # Extract JSON data and create a new State instance
    data = request.get_json()
    instance = State(**data)

    # Save the new State instance to storage
    instance.save()

    # Return the State dictionary as JSON with status 201 Created
    return make_response(jsonify(instance.to_dict()), 201)

# Route to update a specific State by ID
@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """Updates a State"""
    # Get the State object with the specified ID from the storage
    state = storage.get(State, state_id)

    # If State not found, return 404 Not Found
    if not state:
        abort(404)

    # Check if the request contains JSON data
    if not request.get_json():
        abort(400, description="Not a JSON")

    # List of attributes to ignore during the update
    ignore = ['id', 'created_at', 'updated_at']

    # Extract JSON data and update the State attributes
    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(state, key, value)

    # Save the changes to the updated State object
    storage.save()

    # Return the updated State dictionary as JSON with status 200 OK
    return make_response(jsonify(state.to_dict()), 200)
