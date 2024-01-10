#!/usr/bin/python3
"""states api"""
from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage



@app_views.route('/states', methods=['GET'], strict_slashes=False)
def state():
    """get's all states"""
    all_states = storage.all(State)
    content = []
    for key, value in all_states.items():
        content.append(value.to_dict())
    return jsonify(content)


@app_views.route("/states/<string:state_id>", methods=['GET'])
def state_id(state_id):
    """state with id"""
    states = storage.get(State, state_id)
    if states is None:
        abort(404)
    return jsonify(states.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'])
def delete_state(state_id):
    """delete state"""
    states = storage.get(State, state_id)
    if states is None:
        abort(404)
    storage.delete(states)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/', methods=['POST'])
def post_state():
    """post state"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    
    data = request.get_json()
    new_state = State(**data)
    new_state.save()
    
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<string:state_id>", methods=['PUT'])
def update_state(state_id):
    """update state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    
    if not request.get_json():
        abort(400, description="Not a JSON")
    
    data = request.get_json()
    
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    
    state.save()
    
    return jsonify(state.to_dict()), 200
