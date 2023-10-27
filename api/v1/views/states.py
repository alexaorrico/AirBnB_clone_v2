#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects
       And return in json """
    states = []
    for state in storage.all("State").values():
        states.append(state.to_dict())
    return jsonify(states)


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state_by_id(state_id=None):
    """Retrieves a State object by id
           And return in json """
    if state_id:
        for state in storage.all("State").values():
            if state_id == state_id:
                return jsonify(state.to_dict())
        abort(404)


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state_by_id(state_id=None):
    """Deletes a state object by state_id"""
    state_obj = storage.get("State", state_id)
    if state_obj is None:
        abort(404)
    state_obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a state object"""
    if request.json is None:
        return "Not a JSON", 400
    fields = request.get_json()
    if fields.get('name') is None:
        return "Missing name", 400
    new_state = State(**fields)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id=None):
    """Updates a state object by state_id"""
    if request.json is None:
        return "Not a JSON", 400
    fields = request.get_json()
    state_obj = storage.get("State", state_id)
    if state_obj is None:
        abort(404)
    for key in fields:
        if key not in ['id', 'created_at', 'updated_at']:  # ignored keys
            if hasattr(state_obj, key):
                setattr(state_obj, key, fields[key])
    state_obj.save()
    return jsonify(state_obj.to_dict()), 200
