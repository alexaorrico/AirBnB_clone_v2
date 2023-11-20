#!/usr/bin/python3
"""Create a new view for State objects that
handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_state():
    """list of all state objects"""
    all_state_list = list(map(lambda state: state.to_dict(),
                              storage.all(State).values()))
    return jsonify(all_state_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def single_state(state_id):
    """Retrieves state object based on id"""
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)
    else:
        return jsonify(state_obj.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes state object based on id"""
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)
    storage.delete(state_obj)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """Makes a state"""
    obj = request.get_json()
    if not obj:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in obj:
        return make_response(jsonify({"error": "Missing name"}), 400)
    created_state = State(**obj)
    created_state.save()
    return make_response(jsonify(created_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """Updates a State"""
    state_obj = storage.get(State, state_id)
    obj = request.get_json()
    if state_obj is None:
        abort(404)
    if not obj:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in obj.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state_obj, key, value)
    state_obj.save()
    return make_response(jsonify(state_obj.to_dict()), 200)
