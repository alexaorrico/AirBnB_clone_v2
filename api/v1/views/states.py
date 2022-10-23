#!/usr/bin/python3
""" A new view for State objects that handles
all default RESTFul API actions. """
from api.v1.views import app_views
from flask import request, jsonify, abort, make_response
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """ Retrieves the list of all State objects. """
    all_states = storage.all(State).values()
    list_states = [state.to_dict() for state in all_states]

    return jsonify(list_states)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """ Creates a State. """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    state_req = request.get_json()
    if 'name' not in state_req:
        return make_response(jsonify({"error": "Missing name"}), 400)

    state = State(**state_req)
    state.save()

    if storage.get(State, state.id):
        return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state(state_id):
    """ Retrieves a State object. """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    return jsonify(state.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ Deletes a State object. """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    storage.delete(state)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """ Updates a State object. """
    state = storage.get('State', state_id)
    if state is None:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    req_state = request.get_json()
    ignore_keys = ["id", "created_at", "updated_at"]

    for key, value in req_state.items():
        if key not in ignore_keys:
            setattr(state, key, value)

    state.save()
    return make_response(jsonify(state.to_dict()), 200)
