#!/usr/bin/python3
"""Creates a new view for State objects that
handles all default RESTFul API actions"""
from flask import abort, jsonify, request
from models.state import State
from api.v1.views import app_views
from models import storage


# route to get all state objects
@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """returns all state objects"""
    states = storage.all(State).values()
    state_l = [state.to_dict() for state in states]
    return jsonify(state_l)


# route for getting a state obj based on its id
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """returns state obj for the id input"""
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


# route for deleting a file
@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """deletes a state obj"""
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


# route for creating a file
@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """creates a state obj"""
    if not request.get_json():
        abort(400, 'Not a JSON')

    """ transform the HTTP body request to a dictionary"""
    kwargs = request.get_json()
    if name not in kwargs:
        abort(400, 'Missing name')

    state = State(**kwargs)
    state.save()

    return jsonify(state.to_dict()), 201


# route for updating a file
@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """updates a state obj"""
    state = storage.get(State, state_id)
    if state:
        if not request.get_json():
            abort(400, 'Not a JSON')

        """get JSON data from request"""
        new = request.get_json()
        ignore_keys = ['id', 'created_at', 'updated_at']
        """update state obj with json data"""
        for key, value in new.items():
            if key not in ignore_keys:
                setattr(state, key, value)
        state.save()
        return jsonify(state.to_dict()), 200
    else:
        abort(404)
