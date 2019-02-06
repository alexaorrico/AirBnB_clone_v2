#!/usr/bin/python3
""" States RESTful API """

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.base_model import BaseModel
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """ Uses to_dict to retrieve an object into a valid JSON """
    all_states = storage.all("State")
    list = []
    for state in all_states.values():
        list.append(state.to_dict())
    return jsonify(list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def individual_states(state_id):
    """ Retrieves a State object, or returns a 404 if the state_id is not
    linked to any object """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ Deletes a State object, or returns a 404 if the state_id is not
    linked to any object """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ Creates a State object, or returns a 400 if the HTTP body request is not
    valid JSON, or if the dict doesnt contain the key name """
    data = ""
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    name = data.get("name")
    if name is None:
        abort(400, "Missing name")

    new_state = State()
    new_state.name = name
    new_state.save()
    return (jsonify(new_state.to_dict())), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ Updates a State object, or returns a 400 if the HTTP body is not valid
    JSON, or a 404 if state_id is not linked to an object """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    data = ""
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")

    for k, v in data.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(state, k, v)
    state.save()
    return (jsonify(state.to_dict()))
