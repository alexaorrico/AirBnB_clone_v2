#!/usr/bin/python3
"""State route"""
import json

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models import storage


<<<<<<< HEAD
@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id=None):
    """retrieves state [by id | all<default>]"""
    if state_id is None:
        list_all = []
        all_state = storage.all(State)
        for state in all_state.values():
            list_all.append(state.to_dict())
        return jsonify(list_all), 200
    else:
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        return jsonify(state.to_dict()), 200


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id=None):
    """deletes an instance of state from storage"""
=======
@app_views.route('/states', strict_slashes=False)
def get_states():
    """Endpoint to retreive all states"""
    list_states = []
    objs = storage.all(State).values()
    for v in objs:
        v = v.to_dict()
        list_states.append(v)
    return jsonify(list_states)


@app_views.route('/states/<string:state_id>', strict_slashes=False)
def get_state_by_id(state_id):
    """Endpoint to retreive an object by id"""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    obj = obj.to_dict()
    return jsonify(obj)


@app_views.route('/states/<string:state_id>',
                 methods=['GET', 'DELETE'], strict_slashes=False)
def delete_obj(state_id):
    """Endpoint to delete an object"""
    obj = storage.get(State, state_id)
    if not obj:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def add_new_obj():
    """Endpoint to add new objects"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    data = request.get_json()
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<string:state_id>',
                 methods=['PUT', 'GET'], strict_slashes=False)
def update_obj(state_id):
    """Endpoint to update an obj"""
>>>>>>> fbd2a5a9b00d1f1545e7e77f915c60a0af59c718
    state = storage.get(State, state_id)
    if not state:
        abort(404)
<<<<<<< HEAD
    storage.delete(state)
    return jsonify({}), 200


@app_views.route('/states', methods=['POST', 'PUT'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['POST', 'PUT'],
                 strict_slashes=False)
def post_state(state_id=None):
    """creates a new instance of state"""
    req = request.get_json()
    if req is None:
        abort(400, message="Not a JSON")

    if request.method == "POST":
        if 'name' not in req.keys():
            abort(400, message="Missing name")
        else:
            state = State(req)
            return jsonify(state.to_dict()), 201
    elif request.method == "PUT":
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        for i, j in req.items():
            if i not in ["id", "created_at", "updated_at"]:
                setattr(state, i, j)
        storage.save()
        return jsonify(state.to_dict()), 200
=======
    if not request.get_json():
        abort(400, description="Not a JSON")
    for k, v in request.get_json().items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(state, k, v)
    storage.save()
    return jsonify(state.to_dict()), 200
>>>>>>> fbd2a5a9b00d1f1545e7e77f915c60a0af59c718
