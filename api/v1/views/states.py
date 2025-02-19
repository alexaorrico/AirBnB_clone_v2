#!/usr/bin/python3
'''state module'''

from flask import jsonify
from flask import abort, make_response, request
from models.state import State
from models import storage
from api.v1.views import app_views


@app_views.route("/states", strict_slashes=False, methods=["GET"])
def state():
    """returns the list of state objs"""
    states = storage.all(State)
    return jsonify([state.to_dict() for state in states.values()])


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["GET"])
def one_state(state_id):
    """Returns one state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route(
        "/states/<state_id>", strict_slashes=False, methods=["DELETE"])
def del_state(state_id):
    """Delete state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    state.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states", strict_slashes=False, methods=["POST"])
def post_state():
    """Return a new state"""
    if not request.json:
        abort(400, "Not a JSON")
    new_state = request.getjson(silent=True)
    if not new_state:
        abort(400, "Not a JSON")
    if 'name' not in new_state:
        abort(400, "Missing name")
    state = State(**new_state)
    storage.new(state)
    storage.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=["PUT"])
def update_state(state_id):
    """Updates a State object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")

    data = request.get_json()
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(state, key, value)

    state.save()
    return make_response(jsonify(state.to_dict()), 200)
