#!/usr/bin/python3

from flask import Blueprint, jsonify, abort, request
from models.state import State

# Create a Blueprint for the State objects view
states_blueprint = Blueprint('states', __name__)


@states_blueprint.route('/api/v1/states', methods=['GET'])
def list_states():
    """
    Retrieves the list of all State objects.

    Returns:
        JSON response with the list of all State objects.
    """
    # Get all State objects from the database
    # (assuming the State model has a method called 'all()')
    states = State.all()
    # Convert each State object to a dictionary using to_dict()' method
    # and return as JSON
    return jsonify([state.to_dict() for state in states])


@states_blueprint.route('/api/v1/states/<int:state_id>', methods=['GET'])
def get_state(state_id):
    """
    Retrieves a State object by its ID.

    Args:
        state_id (int): The ID of the State to retrieve.

    Returns:
        JSON response with the State object data if found,
        or 404 error if not found.
    """
    # Get the State object with the given state_id from the database
    # (assuming the State model has a method called 'get(state_id)')
    state = State.get(state_id)
    # If the State object is found, return its data as a JSON response
    if state:
        return jsonify(state.to_dict())
    else:
        # If the State object is not found,
        # return a 404 error with a JSON response
        abort(404)


@states_blueprint.route('/api/v1/states/<int:state_id>', methods=['DELETE'])
def delete_state(state_id):
    """
    Deletes a State object by its ID.

    Args:
        state_id (int): The ID of the State to delete.

    Returns:
        JSON response with an empty dictionary and
        200 status code if State is deleted,
        or 404 error if the State object is not found.
    """
    # Get the State object with the given state_id from the database
    # (assuming the State model has a method called 'get(state_id)')
    state = State.get(state_id)
    # If the State object is found, delete it from the database
    # (assuming the State model has a method called 'delete()')
    if state:
        state.delete()
        # Save changes to the database
        # (assuming State model has a method called 'save()')
        state.save()
        return jsonify({}), 200
    else:
        # If the State object is not found,
        # return a 404 error with a JSON response
        abort(404)


@states_blueprint.route('/api/v1/states', methods=['POST'])
def create_state():
    """
    Creates a new State object.

    Returns:
        JSON response with the new State object data and 201 status code.
    """
    # Get the JSON data from the request body
    # using 'request.get_json()' from Flask
    data = request.get_json()
    # If the request body is empty or not a valid JSON,
    # return a 400 error with a JSON response
    if not data:
        abort(400, 'Not a JSON')
    # If the dictionary doesn't contain the key 'name',
    # return a 400 error with a JSON response
    if 'name' not in data:
        abort(400, 'Missing name')
    """ Create a new State object using the JSON data and
    save it to the database (assuming the
    State model has a constructor that accepts **kwargs and
    a method called 'save()') """
    new_state = State(**data)
    new_state.save()
    # Convert the new State object to a dictionary using the 'to_dict()'
    # method and return it with a 201 status code as a JSON response
    return jsonify(new_state.to_dict()), 201


@states_blueprint.route('/api/v1/states/<int:state_id>', methods=['PUT'])
def update_state(state_id):
    """
    Updates an existing State object by its ID.

    Args:
        state_id (int): The ID of the State to update.

    Returns:
        JSON response with the updated State object data and
        200 status code if successful,
        or 404 error if the State object is not found.
    """
    # Get the State object with the given state_id from the db
    # (assuming the State model has a method called 'get(state_id)')
    state = State.get(state_id)
    # If the State object is not found, return a 404 error with a JSON response
    if not state:
        abort(404)
    # Get the JSON data from the request body
    # using 'request.get_json()' from Flask
    data = request.get_json()
    # If the request body is empty or not a valid JSON,
    # return a 400 error with a JSON response
    if not data:
        abort(400, 'Not a JSON')

    # Ignore keys: 'id', 'created_at', and 'updated_at'
    ignored_keys = ['id', 'created_at', 'updated_at']
    # Update the State object with all key-value pairs from JSON data,
    # except for the ignored keys
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(state, key, value)

    # Save the updated State object to the database
    # (assuming the State model has a method called 'save()')
    state.save()
    # Convert the updated State object to a dictionary
    # using the 'to_dict()' method and return it with a 200
    # status code as a JSON response
    return jsonify(state.to_dict()), 200
