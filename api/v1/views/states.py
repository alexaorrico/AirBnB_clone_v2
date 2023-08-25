#!/usr/bin/python3
"""
Create a new view for State objects that
handles all default RESTFul API actions
"""
from flask import Flask, request, jsonify, abort
from models import storage
from api.v1.views import app_views
from models.state import State

app = Flask(__name__)


@app_views.route('/states/', methods=['GET'])
def get_states():
    store_states = storage.all(State)
    list_states = []
    for state in store_states:
        list_states.append(store_states[state].to_dict())
    return jsonify(list_states), 200


@app_views.route('/states/', methods=['POST'])
def post_states():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400
    new_state = State()
    new_state.name = data['name']
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['GET'])
def get_states_id(state_id):
    store_states = storage.get(State, state_id)
    if store_states is None:
        return abort(404)
    return jsonify(store_states.to_dict()), 200


@app_views.route('/states/<state_id>', methods=['PUT'])
def put_states_id(state_id):
    data = request.get_json()

    store_state_id = storage.get(State, state_id)
    if store_state_id is None:
        return abort(404)
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(store_state_id, key, value)
    store_state_id.save()
    return jsonify(store_state_id.to_dict()), 200


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_states_id(state_id):
    to_delete = storage.get(State, state_id)
    if to_delete is None:
        return abort(404)
    storage.delete(to_delete)
    storage.save()
    return jsonify({}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
