#!/usr/bin/python3
""" Handles all State requests for the API """

from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
from models.state import State
from models import storage


@app_views.route('/states', strict_slashes=False)
def all_states():
    """ Returns a JSON of all State objects """
    states = []
    for obj in storage.all(State).values():
        states.append(obj.to_dict())
    return jsonify(states), 201


@app_views.route('/states/<string:state_id>', strict_slashes=False)
def one_state(state_id):
    """ Returns a JSON of a state whose id was requested """
    obj = storage.get(State, state_id)
    if obj is not None:
        return jsonify(obj.to_dict())
    return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ Deletes an obj whose id was passed """
    obj = storage.get(State, state_id)
    if obj is None:
        return make_response(jsonify({"error": "Not found"}), 404)
    obj.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def add_state():
    """ Creates a new state obj into the db """
    post_data = request.get_json()
    if post_data is None:
        abort(400, "Not a JSON")
    if "name" not in post_data.keys():
        abort(400, "Missing name")
    obj = State(**post_data)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """ Updates a state obj with the dict from HTTP request """
    obj = storage.get(State, state_id)
    if obj is None:
        return make_response(jsonify({"error": "Not found"}), 404)
    put_data = request.get_json()
    if put_data is None:
        abort(400, "Not a JSON")
    for key, value in put_data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(obj, key, value)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 200)
