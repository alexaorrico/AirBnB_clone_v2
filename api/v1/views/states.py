#!/usr/bin/python3
""" State objects RESTFul API. """
from flask import jsonify, request, abort
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def getting_states():
    """ Retrieves list of all State objs. """
    states = storage.all(State).values()
    list_of_states = [state.to_dict() for state in states]
    return jsonify(list_of_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state_by_id(state_id):
    """ Returns a state based from it's ID. """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ Deletes state based on id. """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def creates_a_state():
    """ Creates a State. """
    HTTP_body = request.get_json(silent=True)
    if not HTTP_body:
        abort(400, 'Not a JSON')
    if 'name' not in HTTP_body:
        abort(400, 'Missing name')
    latest_state = State(**HTTP_body)
    storage.new(latest_state)
    storage.save()
    return jsonify(latest_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def updating_state(state_id):
    """ Updating a State obj. """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    HTTP_body = request.get_json(silent=True)
    if not HTTP_body:
        abort(400, 'Not a JSON')
    ignoring_keys = ['id', 'created_at', 'updated_at']
    for key, value in HTTP_body.items():
        if key not in ignoring_keys:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
