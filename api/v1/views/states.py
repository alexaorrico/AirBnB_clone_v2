#!/usr/bin/python3
"""Module"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from flask import make_response, abort, request
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """
    Retrieves the list of all State objects: GET /api/v1/states
    In JSON format
    """
    states = storage.all(State).values()
    list_states = []
    for state in states:
        list_states.append(state.to_dict())
    return jsonify(list_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def states_id(state_id):
    """Retrieves a State object: GET /api/v1/states/<state_id>"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """DELETE state based on id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Returns the new State with the status code 201"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    req_body = request.get_json()
    object = State(**req_body)
    storage.new(object)
    storage.save()
    return make_response(jsonify(object.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a State object: PUT /api/v1/states/<state_id>"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    req_body = request.get_json()
    exempt = ["id", "created_at", "updated_at"]

    for key, value in req_body.items():
        if key not in exempt:
            setattr(state, key, value)
        else:
            pass

    storage.save()
    return make_response(jsonify(state.to_dict()), 200)