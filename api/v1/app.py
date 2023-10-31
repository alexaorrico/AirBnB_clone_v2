from api.v1.views import app_views
from flask import Flask, jsonify, request
from models.state import State
from models import storage

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    states = storage.all(State)
    return jsonify([state.to_dict() for state in states.values()])

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({})

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    if not request.json:
        abort(400, "Not a JSON")
    if "name" not in request.json:
        abort(400, "Missing name")
    state = State(**request.json)
    state.save()
    return jsonify(state.to_dict()), 201

@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    for key, value in request.json.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict())

