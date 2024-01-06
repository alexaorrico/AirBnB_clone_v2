#!/usr/bin/python3
""" The module handles the default RESTful API acstions """

# Import the required Modules
from flask import abort, jsonify, request
from models.state import State
from api.v1.views import app_views
from models import storage

# Route for retrieving all state objs
@app_views.route('/state', method=['GET'], strict_slashes=False)
def get_all_states:
    """
    GETs all state objects
    """
    states = storage.all(State).values()
    state_list = [state.to_dict() for state in states]
    return jsonify(state_list)

# Route for retrieving specific stated by thier id
@app_views.route('/state/<state_id>', method=['GET'], strictslashes=False)
def get_state(state_id):
    """
    GETs a specified state
    """
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict)
    else:
        abort(404)

# Route for deleting a specific State by id
@app_views.route('/states/<state_id>', method=['DELETE'])
def delete_state(state_id):
    """
    DELETEs a state by thier id
    """
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        return jsonify({}), 200
    else:
        abort(404)

# Route for creating a new state
@app_views.route('/states', method=['POST'], strict_slashes=False)
def create_state:
    """ PUTs in a new state """
    if not request.get_json:
        abort(400, 'Not a JSON')

    kwargs = request.get_json
    if 'name' not in kwargs:
        abort(400, 'Missing name')

    state = State(**kwargs)
    state.save()
    return jsonify(state.to_dict()), 201

# Route for updating an existing state
@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """
    Updates an existing state
    """
    state = storage.get(State, state_id)
    if state:
        if not request.get.json():
            abort(400, 'Not a JSON')

        data = request.get_json()
        ignore_keys = ['id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(state, key, value)
        state.save()
        return jsonify(state.to_dict()), 200
    else:
        abort(404)


# Error Handlers
@app_views.errorhandler(404)
def not_found(error):
    """ Handles the 404 code """
    response = {'error': 'Not found'}
    return jsonify(response), 404

@app_views.errorhandler(400)
def bad_request(error):
    """ Handles the 400 status code """
    response = {'error': 'Bad Request'}
    return jsonify(response), 400
