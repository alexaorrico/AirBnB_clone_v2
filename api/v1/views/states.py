#!/usr/bin/python3
""" States Module"""

from models import storage
from flask import abort, jsonify, request, make_response
from api.v1.views import app_views
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """
    Retrieves the list of all State objects
    """
    states = []
    for state in storage.all("State").values():
        states.append(state.to_dict())
    return jsonify(states)


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_state(state_id):
    """
    Retrieves a State object by id
    """
    state = storage.get("State", state_id)
    if state:
        return jsonify(state.to_dict())
    abort(404)


@app_views.route("/states", methods=['POST'], strict_slashes=False)
def create_state():
    """
    Create a new State instance
    """
    if not request.json:
        abort(400, "Not a JSON")
    if 'name' not in request.json:
        abort(400, "Missing name")
    state = models.state.State(name=request.json['name'])
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """
    Update a State instance
    """
    if not request.json:
        abort(400, "Not a JSON")
    state = storage.get("State", id=state_id)
    if state:
        state.name = request.json['name']
        state.save()
        return jsonify(state.to_dict()), 200
    abort(404)


@app_views.route("/states/<state_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """
    Delete a State instance
    """
    state = storage.get("State", id=state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    abort(404)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
