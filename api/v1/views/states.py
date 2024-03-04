#!/usr/bin/python3
"""
View for State objects that handles all default RESTFul API actions.
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage, State
from werkzeug.exceptions import BadRequest


@app_views.route("/states", strict_slashes=False)
def get_states_objects():
    """returns: a list of all state objects"""
    states = storage.all(State)
    states_list = []
    for state in states.values():
        states_list.append(state.to_dict())
    return states_list


@app_views.route("states/<state_id>", strict_slashes=False)
def get_state_object(state_id):
    """returns: an object of a specified id"""
    states = storage.all(State)
    for state in states.values():
        if state.id == state_id:
            return state.to_dict()
    # obj not found
    abort(404)


@app_views.route("/states/<state_id>",
                 methods=['DELETE'], strict_slashes=False)
def delete_state_object(state_id):
    """delete: a state object"""
    states = storage.all(State)
    for state in states.values():
        if state.id == state_id:
            # delete obj and save changes to storage
            storage.delete(state)
            storage.save()
            return jsonify({}), 200
    # obj not found
    abort(404)


@app_views.route("/states", methods=['POST'], strict_slashes=False)
def create_state_object():
    """create: a state object"""
    try:
        data = request.get_json()
    except BadRequest:
        abort(400, "Not a JSON")
    if 'name' not in data:
        abort(400, 'Missing name')
    # create state object
    new_state = State(**data)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=['PUT'], strict_slashes=False)
def update_obj(state_id):
    """update: a state object"""
    states = storage.all(State)
    for state in states.values():
        if state.id == state_id:
            try:
                data = request.get_json()
            except BadRequest:
                abort(400, 'Not a JSON')
            for k, v in data.items():
                if k == 'id' or k == 'created_at' or k == 'updated_at':
                    continue
                setattr(state, k, v)
            # save changes to storage
            storage.save()
            return jsonify(state.to_dict()), 201
    # object not found
    abort(404)
