#!/usr/bin/python3
"""index default view"""

from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", strict_slashes=False)
def all_states():
    """retrieves all state objects by class name"""
    states = []
    for state in storage.all('State').values():
        states.append(state.to_dict())
    return jsonify(states)


@app_views.route("/states/<state_id>", strict_slashes=False)
def state(state_id):
    """retrieves the class obj by id"""
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", strict_slashes=False, methods=['DELETE'])
def delete_state(state_id):
    """deletes state by id"""
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states", methods=["POST"])
def create_state():
    '''Creates the required test case'''
    if not request.get_json():
        abort(400, description="Not a JSON")

    if not request.get_json().get('name'):
        abort(400, description="Missing name")

    state = State()
    state.name = request.get_json()['name']
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=['PUT'])
def update_state(state_id):
    '''Updates the state with the id passed'''
    state = storage.get("State", state_id)
    if not state:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    for k, v in request.get_json().items():
        if k == "id" or k == "created_at" or k == "updated_at":
            continue
        else:
            setattr(state, k, v)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
