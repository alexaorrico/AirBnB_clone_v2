#!/usr/bin/python3
""" States Module"""


from models.state import State
from models import storage
from flask import Flask, abort, jsonify, request, json
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """    Retrieves the list of all State objects
    """
    states = []
    for key, value in storage.all("State").items():
        states.append(value.to_dict())
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
    if request.is_json:
        dicc = request.get_json()
    else:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' in dicc:
        new_state = State()
        new_state.name = dicc["name"]
        storage.new(new_state)
        storage.save()
        return jsonify(new_state.to_dict()), 201
    else:
        return jsonify({"error": "Missing name"}), 400


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
