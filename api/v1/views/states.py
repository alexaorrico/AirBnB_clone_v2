#!/usr/bin/python3
""" States Views """
from flask import jsonify, abort, request, Response, make_response
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states_all():
    """
    Return all states
    """
    all_states = storage.all('State').values()
    states = []
    for obj in all_states:
        states.append(obj.to_dict())

    return jsonify(states)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """
    post a State object
    """
    if not request.json:
        abort(400, "Not a JSON")
    data = request.json
    if 'name' not in data.keys():
        abort(400, "Missing name")
    instance = State(**data)
    storage.new(instance)
    storage.save()

    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def list_states(state_id):
    """
    Retrieves a State object
    """
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    state = state.to_dict()

    return jsonify(state)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """
    deletes a State object
    """
    state = storage.get('State', state_id)
    if state is None:
        abort(404)

    storage.delete(state)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """
    update a State object
    """
    state = storage.get('State', state_id)
    if state is None:
        abort(404)

    if not request.json:
        abort(400, "Not a JSON")

    data = request.json
    for key, value in data.items():
        setattr(state, key, value)

    storage.save()

    return make_response(jsonify(state.to_dict()), 200)
