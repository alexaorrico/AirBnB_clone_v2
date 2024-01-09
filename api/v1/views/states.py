#!/usr/bin/python3
"""states api"""
from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage


all_states = storage.all(State)


@app_views.route("/states/", methods=['GET'])
@app_views.route('/states', methods=['GET'])
def state():
    """get's all states"""
    content = []
    for key, value in all_states.items():
        content.append(value.to_dict())
    return jsonify(content)


@app_views.route("/states/<string:state_id>", methods=['GET'])
def state_id(state_id):
    for key, value in all_states.items():
        newkey = key.split('.')[1]
        if state_id == newkey:
            return jsonify(value.to_dict())
    abort(404)


@app_views.route('/states/<string:state_id>', methods=['DELETE'])
def delete_state(state_id):
    for key, value in all_states.items():
        if state_id in key:
            return {}, 200
    abort(404)


@app_views.route('/states/', methods=['POST'])
def post_state():
    try:
        message = request.get_json()
    except Exception:
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        return abort(400, "Missing name")
    
    data = request.get_json()
    state = State(**data)
    return jsonify(state.to_dict()), 201


@app_views.route("/states/<string:state_id>", methods=['PUT'])
def update_state(state_id):
    try:
        message = request.get_json()
    except Exception:
        abort(400, description="Not a JSON")
    for key, value in all_states.items():
        newkey = key.split('.')[1]
        if state_id == newkey:
            end = False
            break
        end = True
    if end:
        abort(404)
    for key, value in message.items():
        if key in ['id', 'created_at', 'updated_at']:
            continue
        state = State(key=value)
    return jsonify(state.to_dict()), 200
