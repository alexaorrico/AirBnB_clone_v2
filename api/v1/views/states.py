"""Module providing API endpoints for State resources."""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieve a list of all states."""
    states_list = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(states_list)

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieve information about a specific state."""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Delete a state by its ID."""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Create a new state."""
    if request.is_json:
        data = request.get_json()
        state = State()
        if 'name' not in data:
            return jsonify({"error": "Missing name"}), 400
        else:
            state.name = data["name"]
            storage.new(state)
            storage.save()
            return jsonify(state.to_dict()), 201
    else:
        return jsonify({"error": "Not a JSON"}), 400

@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """Update a state's information."""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.is_json:
        data = request.get_json()
        keys_to_ignore = ['id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in keys_to_ignore:
                setattr(state, key, value)
        state.save()
        return jsonify(state.to_dict()), 200
    else:
        return jsonify({"error": "Not a JSON"}), 400
