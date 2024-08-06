#!/usr/bin/python3
"""handles all default RESTFul API actions for State objects"""

from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_states():
    '''
        Retrieves the list of all State objects
    '''
    states_dict = storage.all(State)
    return jsonify([objct.to_dict() for objct in states_dict.values()])

@app_views.route("/states/<string:state_id>", methods=["GET"], strict_slashes=False)
def get_state(state_id):
    '''
        retrieve one State object
    '''
    state = storage.get(State, state_id)

    # check if state object exists
    if state is None:
        abort(404)

    return jsonify(state.to_dict())

@app_views.route(
    "/states/<string:state_id>", methods=["DELETE"], strict_slashes=False)
def delete_state(state_id):
    '''
        Delete a State object
    '''
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    state.delete()
    storage.save()

    return make_response(jsonify({}), 200)

@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    '''
        Create a State object
    '''
    data_state = request.get_json()

    if not data_state:
        abort(400, "Not a JSON")
    elif "name" not in data_state.keys():
        abort(400, "Missing name")
    else:
        data_state = State(**data_state)
        data_state.save()

    # return the new state object with CREATED status code 201
    return make_response(jsonify(data_state.to_dict()), 201)

@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """
        Updates a State
    """
    state_O = storage.get(State, state_id)

    if not state_O:
        abort(404)

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    ignore_keys = ['id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore_keys:
            setattr(state_O, key, value)

    storage.save()

    return jsonify(state_O.to_dict())
