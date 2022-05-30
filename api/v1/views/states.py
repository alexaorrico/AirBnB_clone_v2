#!/usr/bin/python3
""" State view """
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """ Retrieves the list of all State objects """
    states = storage.all(State)
    return jsonify([obj.to_dict() for obj in states.values()])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state_id(state_id):
    """ Retrieves a State object """
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def state_delete(state_id):
    """ Deletes a State object """
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def state_post():
    """ Create a new state """
    new_state = request.get_json()
    if new_state is None:
        abort(400, 'Not a JSON')
    if 'name' not in new_state:
        abort(400, 'Missing name')
    state = State(**new_state)
    storage.new(state)
    storage.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def state_id_put(state_id):
    """ Updates a State object """
    state = storage.get('State', state_id)
    if not state:
        abort(404)
    request_json = request.get_json()
    if not request_json:
        abort(400, "Not a JSON")
    for k, v in request_json.items():
        if k != 'id' and k != 'created_at' and k != 'updated_at':
            setattr(state, k, v)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
