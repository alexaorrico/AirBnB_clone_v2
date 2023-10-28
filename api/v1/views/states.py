#!/usr/bin/python3
""" Create new view for State """

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.state import State
from models.engine.db_storage import classes


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """ Retrieves list of all State """
    states = storage.all(State).values()
    # Convert objects to dictionaries & jsonify list
    state_list = [state.to_dict() for state in states]
    return jsonify(state_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """ Retrieves a State """
    # Get State with given ID from storage
    state = storage.get(State, state_id)
    if state:
        # Return the State in JSON format
        return jsonify(state.to_dict())
    else:
        # Return (ERROR 404) -> if State isn't found
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """ Deletes a State """
    state = storage.get(State, state_id)
    if state:
        # Delete State from storage & save all changes
        storage.delete(state)
        storage.save()
        # Return Empty JSON with -> 200 status code
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ Creates a State """
    if not request.get_json():
        # Return (ERROR 404) -> if Request data isn't in JSON format
        abort(400, 'Not a JSON')

    # Get JSON data from Request
    kwargs = request.get_json()
    if 'name' not in kwargs:
        # Return (ERROR 404) -> if 'name' key is missing in JSON data
        abort(400, 'Missing name')

    # Create new State with JSON data & Save to storage
    state = State(**kwargs)
    state.save()
    # Return newly created State in JSON format with status -> (code 201)
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ Updates a State """
    state = storage.get(State, state_id)
    if state:
        if not request.get_json():
            abort(400, 'Not a JSON')

        data = request.get_json()
        ignore_keys = ['id', 'created_at', 'updated_at']
        # Update attributes of State with JSON data & Save to storage
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(state, key, value)
        state.save()
        # Return updated State in JSON format with status -> (code 200)
        return jsonify(state.to_dict()), 200
    else:
        abort(404)


@app_views.errorhandler(404)
def not_found(error):
    """ Raises ERROR 404 """
    return jsonify({'error': 'Not found'}), 404


@app_views.errorhandler(400)
def bad_request(error):
    """ Returns Bad Request Message for Illegal Requests to API """
    return jsonify({'error': 'Bad Request'}), 400
