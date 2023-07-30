#!/usr/bin/python3
""" View for State objects that handles all default RESTFul API actions """
from . import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State


@app_views.route("/states", method = ["GET"], strict_slashes=False)
def all_states():
    """Retrieves a list of all states """
    states_dict = storage.all("State")
    return jsonify([obj.to_dict() for obj in states_dict.values()])


@app_views.route("/states/<state_id>", method = ["GET"], strict_slashes=False)
def get_state(state_id):
    """Retrieves a state by its id """
    state_obj = storage.get("State", state_id)
    if not state_obj:
        abort(404)
    return jsonify(state_obj.to_dict())


@app_views.route("/states/<state_id>",
                 methods=['DELETE'], strict_slashes=False)
def del_state(state_id):
    """ Deletes a state """
    state_obj = storage.get("State", state_id)
    if not state_obj:
        abort(404)
    storage.delete(state_obj)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """ Creates a State """
    data = request.json
    if not data:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    state_obj = State(**request.get_json())
    state_obj.save()
    return make_response(jsonify(state_obj.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """ Updates a State object"""
    state_obj = storage.get("State", state_id)
    if not state_obj:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in['id', 'created_at', 'updated_at']:
            setattr(state_obj, key, value)
    state_obj.save()
    return make_response(jsonify(state_obj.to_dict()), 200)
