#!/usr/bin/python3

"""
Hanles all default RESTFul API actions
"""


from flask import abort, jsonify, request
from models.state import State
from api.v1.views import app_views
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """
    Retrives all states objects
    """
    states = storage.all(State).values()

    retrive_states = []
    for state in states:
        retrive_states,append(state.to_dict())

    return jsonify(retrive_states)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create_new_state():
    """
    Create a new state object
    """
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in  request.get_json():
        abort(400, 'Missing name')

    # create new state with JSON 
    state_obj = State(request.get_json())
    state_obj.save()

    return jsonify(state_obj.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """
    Retrives a state by a given id
    """
    state_obj = storage.get(State, state_id)
    
    if state_obj:
        return jsonify(state_obj.to_dict())
    else:
        return abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    state_obj = storage.get(State, state_id)
    if state_obj:
        storage.delete(state_obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update_state(state_id):
    """
    Update the state object given by id
    """
    state_obj = storage.get(State, state_id)
    if state_obj:
        if not request.get_json():
            # Return 400 error if the request data is not in JSON format
            abort(400, 'Not a JSON')

        data = request.get_json()
        ignore_keys = ['id', 'created_at', 'updated_at']
        # Update the attributes of the State object with the JSON data
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(state_obj, key, value)

        # Save the updated State object to the storage
        state_obj.save()
        # Return the updated State object in JSON format with 200 status code
        return jsonify(state_obj.to_dict()), 200
    else:
        # Return 404 error if the State object is not found
        abort(404)
