#!/usr/bin/python3
"""states views"""
from models.state import State
from flask import abort, request, jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/states/<state_id>', methods=['GET'])
@app_views.route('/states', defaults={'state_id': None}, methods=['GET'])
def retrives_state(state_id):
    """Retrives the list of all states"""
    if state_id is None:
        # 1 option:
        # states_list = []
        # states = storage.all(State)
        # for state in states.values():
        #     states_list.append(state.to_dict())
        # return states_list
        # 2 option:
        # return list(map(lambda x: x.to_dict(), storage.all(State)))
        # 3 opttion
        return jsonify([
            state.to_dict() for state in storage.all(State).values()])

    if storage.get(State, state_id) is None:
        abort(404)

    return jsonify(storage.get(State, state_id).to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Delete state"""
    states = storage.get(State, state_id)
    if states is None:
        abort(404)
    states.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'])
def create_state():
    """creates a new state"""
    json_data = request.get_json()
    if json_data is None:
        abort(400, 'Not a JSON')
    if 'name' not in json_data:
        abort(400, 'Missing name')
    state = State(**json_data)
    state.save()
    # return a tuple default(data, status)
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """update a state"""
    json_data = request.get_json()
    if json_data is None:
        abort(400, 'Not a JSON')
    state = storage.get(State, state_id)
    for key, values in json_data.items():
        if key not in ('id', 'created_at', 'updated_at'):
            setattr(state, key, values)
    state.save()
    return jsonify(state.to_dict()), 200
