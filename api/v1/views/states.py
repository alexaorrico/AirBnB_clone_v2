#!/usr/bin/python3
"""handles all default RESTFul API actions"""
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route("/states", methods=["GET"], strict_slashes=False)
@swag_from("documentation/state/get.yml", methods=["GET"])
def get_all_states():
    """
    Retrieves the list of all State objects
    """
    all_states = storage.all(State).values()
    list_states = []
    for state in all_states:
        list_states.append(state.to_dict())
    return jsonify(list_states)


@app_views.route("/states/<string:state_id>", methods=["GET"], strict_slashes=False)
@swag_from("documentation/state/get_id.yml", methods=["GET"])
def get_state_id(state_id):
    """Retrieves a specific state by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<string:state_id>", methods=["DELETE"], strict_slashes=False)
@swag_from("documentation/state/delete.yml", methods=["DELETE"])
def delete_state(state_id):
    """Deletes a  state by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
@swag_from("documentation/state/post_state.yml", methods=["POST"])
def post_state():
    """
    Creates a State
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if "name" not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)

    body = request.get_json()
    instance = State(**body)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)
