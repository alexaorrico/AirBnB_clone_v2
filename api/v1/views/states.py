#!/usr/bin/python3
"""State API"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State


@app_views.route("/states", strict_slashes=False, methods=['GET'])
@app_views.route("/states/<string:state_id>", strict_slashes=False,
                 methods=['GET'])
def get_states(state_id=None):
    """Returns all states objects or a given state"""
    if state_id is not None:
        state = storage.get(State, state_id)
        if state is not None:
            return jsonify(state.to_dict())
        else:
            return jsonify({'error': 'Not found'}), 404
    states = list(storage.all(State).values())
    return jsonify([state.to_dict() for state in states])


@app_views.route("/states/<string:state_id>", strict_slashes=False,
                 methods=['DELETE'])
def delete_state(state_id):
    """Delete a state"""
    state = storage.get(State, state_id)
    if state is not None:
        state.delete()
        return jsonify({})
    abort(404)


@app_views.route("/states/", strict_slashes=False,
                 methods=['POST'])
def create_state():
    """Create a state"""
    if request.is_json:
        data = request.get_json()
        state_name = data.get('name', None)
        if state_name is None:
            abort(400, description='Missing name')
        state = State(name=state_name)
        state.save()
        return jsonify(state.to_dict()), 201
    abort(400, description='Not a JSON')


@app_views.route("/states/<string:state_id>", strict_slashes=False,
                 methods=['PUT'])
def update_state(state_id):
    """Updates a state"""
    if request.is_json:
        state = storage.get(State, state_id)
        if state is not None:
            data = request.get_json()
            data = {k: v for k, v in data.items() if k != 'id' and
                    k != 'created_at' and k != 'updated_at'}
            for k, v in data.items():
                setattr(state, k, v)
            state.save()
            return jsonify(state.to_dict()), 200
        abort(404)
    abort(400, description='Not a JSON')
