#!/usr/bin/python3
""" A new view for State objects that handles
all default RESTFul API actions. """
from api.v1.views import app_views
from flask import request, jsonify, abort, make_response
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """ Retrieves the list of all State objects. """
    all_states = storage.all('State').values()
    list_states = []
    for state in all_states:
        list_states.append(state.to_dict())

    return jsonify(list_states)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """ Creates a State. """
    if not request.json:
        abort(400, "Not a JSON")
    state_req = request.json
    if 'name' not in state_req:
        abort(400, "Missing name")
    state = State(**data)
    storage.new(state)
    storage.save()

    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """ Retrieves a State object. """
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    state = state.to_dict()

    return jsonify(state)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ Deletes a State object. """
    state = storage.get('State', state_id)
    if state is None:
        abort(404)

    storage.delete(state)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ Updates a State object. """
    state = storage.get('State', state_id)
    if state is None:
        abort(404)

    if not request.json:
        abort(400, "Not a JSON")

    req_state = request.json
    for key, value in req_state.items():
        setattr(state, key, value)

    storage.save()

    return make_response(jsonify(state.to_dict()), 200)
