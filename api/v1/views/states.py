#!/usr/bin/python3
""""""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.base_model import BaseModel
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves all State objects"""
    list_states = []
    for state in storage.all('State').values():
        list_states.append(state.to_dict())
    return jsonify(list_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieve one State object"""
    key_st = 'State.' + state_id
    my_dict = storage.all('State')
    if key_st in my_dict:
        return jsonify(my_dict[key_st].to_dict())
    else:
        abort(404)


@app_views.route('/states/<string:state_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Delete a State object"""
    if state_id:
        empty_dict = {}
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        state.delete()
        storage.save()
        return jsonify(empty_dict)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Create a State object"""
    my_dict = request.get_json()
    if my_dict is None:
        abort(400, "Not a JSON")
    elif "name" not in my_dict:
        abort(400, "Missing name")
    new_state = State(**my_dict)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<string:state_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """Update a State object"""
    if state_id:
        my_dict = request.get_json()
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        if my_dict is None:
            abort(400, "Not a JSON")
        for key, value in my_dict.items():
                if key not in ["id", "created_at", "updated_at"]:
                    setattr(state, key, value)
        storage.save()
        return jsonify(state.to_dict()), 200
