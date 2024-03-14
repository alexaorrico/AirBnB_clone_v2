#!/usr/bin/python3
""" Handles all State requests for the API """

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.state import State
from models import storage


@app_views.route('/states', strict_slashes=False)
def all_states():
    """ Returns a JSON of all State objects """
    states = []
    for obj in storage.all(State).values():
        states.append(obj.to_dict())
    return make_response(jsonify(states), 200)


@app_views.route('/states/<state_id>', methods=['GET'],
                 strict_slashes=False)
def one_state(state_id):
    """ Returns a JSON of a state whose id was requested """
    obj = storage.get(State, state_id)
    if obj:
        return make_response(jsonify(obj.to_dict()), 200)
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ Deletes an obj whose id was passed """
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    obj.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def add_state():
    """ Creates a new state obj into the db """
    if request.is_json is True:
        post_data = request.get_json()
        if "name" in post_data.keys():
            obj = State(**post_data)
            storage.new(obj)
            storage.save()
            return make_response(jsonify(obj.to_dict()), 201)
        abort(400, "Missing name")
    abort(400, "Not a JSON")


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """ Updates a state obj with the dict from HTTP request """
    if request.is_json is True:
        put_data = request.get_json()
        obj = storage.get(State, state_id)
        if obj:
            for key, value in put_data.items():
                if key not in ["id", "created_at", "updated_at"]:
                    setattr(obj, key, value)
            obj.save()
            return make_response(jsonify(obj.to_dict()), 200)
        abort(404)
    abort(400, "Not a JSON")
