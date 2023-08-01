#!/usr/bin/python3
""" holds class State"""
from flask import Blueprint, jsonify, request
from models.state import State
# new view for State objects that handles all default RESTFul API actions


# create a Blueprint for the State objects view
# 'states' is the Blueprint name
# __name__ is the module that will use this Blueprint
states_blueprint = Blueprint('states', __name__)


# Route to retrieve the list of all State objects
@states_blueprint.route('/api/v1/states', methods=['GET'])
def get_states():
    # Retrieves the list of all State objects: GET /api/v1/states
    states = State.all()
    # Convert the list of State objects to a dictionary
    # using the 'to_dict()' method
    # Return the dictionary as a JSON response with the status code 200
    return jsonify([state.to_dict() for state in states]), 200

# Route to retrive a single State object by its ID
@states_blueprint.route('/api/v1/states/<int:state_id>', methods=['GET'])
def get_state(state_id):
    # Retrieves a State object: GET /api/v1/states/<state_id>
    state = State.get(state_id)
    if not State:
        return jsonify({"message": "State not found"}), 404
    # Convert State object to dictionary using 'to_dict()' method
    # return it as a JSON response with the 200 status code.
    return jsonify(state.to_dict()), 200


# Route to delete a State object by its ID
@states_blueprint.route('/api/v1/states/<int:state_id>', methods=['DELETE'])
def delete_state(state_id):
    # Deletes a State object: DELETE /api/v1/states/<state_id>
    # Get the State object with the given state_id from the database
    # (assuming the State model has a method called 'get(state_id)')
    state = State.get(state_id)
    if not State:
        return jsonify({"message": "Not found"}), 404
    # Delete the State object from the database
    # (assuming the State model has a method called 'delete()')
    state.delete()
    # Return an empty dictionary with the status code 200
    return jsonify({}), 200


# Route to create a State object
@states_blueprint.route('/api/v1/states', methods=['POST'])
def post_state(state_id):
    # Creates a State: POST /api/v1/states
    # You must use request.get_json from Flask transform
    # HTTP body request to a dictionary

    # If the HTTP body request is not valid JSON,
    # raise a 400 error with the message Not a JSON

    # If the dictionary doesn’t contain the key name,
    # raise a 400 error with the message Missing name
    # Returns the new State with the status code 201
    data = request.get_json()
    if not data:
        return jsonify({"message": "Not a JSON"}), 400
    if 'name' not in data:
        return jsonify({"message": "Missing name"}), 400
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@states_blueprint.route('/api/v1/states/<int:state_id>', methods=['PUT'])
def put_state(state_id):
    # Updates a State object: PUT /api/v1/states/<state_id>
    state = State.get(state_id)
    if not State:
        return jsonify({"message": "Not found"}), 404
    # Get JSON data from request body
    # using 'request.get_json()' from Flask
    data = request.get_json()
    # If request body is empty or not valid JSON,
    # return 400 error with JSON response containing message Not a JSON
    if not data:
        return jsonify({"message": "Not a JSON"}), 400

    # Ignore keys: 'id', 'created_at', and 'updated_at'
    ignore_keys = ['id', 'created_at', 'updated_at']
    # Update the State object from the database using
    # the keys and values in the dictionary
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(state, key, value)

    # Save the updated State object to the database
    # (assuming the State model has a method called 'save()')
    state.save()
    # Convert the updated State object to a dictionary
    # using the 'to_dict()' method and return it with
    # a 200 status code as JSON response
    return jsonify(state.to_dict()), 200
