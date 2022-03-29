#!/usr/bin/python3
""" View for States """


from api.v1.views import app_views
from flask import jsonify, abort, request
import models


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def all_states_id(state_id):
    """ Return all states """
    state = models.storage.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['DELETE'])
def a_state(state_id):
    """ Delete a state """
    state = models.storage.get("State", state_id)
    if state is None:
        abort(404)
    models.storage.delete(state)
    models.storage.save()
    return jsonify({}), 200


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create_state():
    """ Create a state """
    if not request.json:
        abort(400, 'Not a JSON')
    if 'name' not in request.json:
        abort(400, 'Missing name')
    state = models.State(**request.json)
    models.storage.new(state)
    models.storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update_state(state_id):
    """ Update a state """
    state = models.storage.get("State", state_id)
    if state is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    for key, value in request.json.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(state, key, value)
    models.storage.save()
    return jsonify(state.to_dict()), 200
