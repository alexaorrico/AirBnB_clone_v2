#!/usr/bin/python3
""" Methos API for object States """
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route('/states', defaults={'state_id': None},
                 methods=['GET'],
                 strict_slashes=False)
@app_views.route('/states/<path:state_id>')
def get_state(state_id):
    """ Get all or one State object """
    if state_id is None:
        all_states = storage.all(State)
        return jsonify([state.to_dict() for state in all_states.values()])

    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ Delete a State object """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    state.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """ Create a new State object """
    request_state = request.get_json()
    if not request_state:
        abort(400, "Not a JSON")
    if "name" not in request_state:
        abort(400, "Missing name")
    state = State(**request_state)
    storage.new(state)
    storage.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """ Update a State object """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    request_state = request.get_json()
    if not request_state:
        abort(400, "Not a JSON")

    for key, value in request_state.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
