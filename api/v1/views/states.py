#!/usr/bin/python3
""" STATE VIEW """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models import storage


@app_views.route(
    '/states', methods=["GET"], strict_slashes=False
)
def all_states():
    """ Return all states objects in DB """
    all_states = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(all_states)


@app_views.route(
    '/states/<state_id>', methods=["GET"], strict_slashes=False
)
def single_state(state_id):
    """ Returns state that matches with provided ID """
    state = storage.get(State, str(state_id))
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route(
    '/states/<state_id>', methods=["DELETE"], strict_slashes=False
)
def delete_state(state_id):
    """ Deletes state that matches with provided ID """
    sta = storage.get(State, str(state_id))
    if sta is None:
        abort(404)

    storage.delete(sta)
    storage.save()
    return jsonify({})


@app_views.route(
    '/states/', methods=["POST"], strict_slashes=False
)
def add_state():
    """ Adds state object to DB """
    data = request.get_json(silent=True)
    if data is None:
        abort(400, 'Not a JSON')
    if "name" not in data:
        abort(400, 'Missing name')

    new_state = State(**data)
    storage.new(new_state)
    storage.save()
    res = jsonify(new_state.to_dict())
    res.status_code = 201
    return res


@app_views.route(
    '/states/<state_id>', methods=["PUT"], strict_slashes=False
)
def update_state(state_id):
    """Updates state object"""
    data = request.get_json(silent=True)
    if data is None:
        abort(400, 'Not a JSON')
    state = storage.get(State, str(state_id))
    if state is None:
        abort(404)

    for key, val in data.items():
        if key not in ["id", "updated_at", "created_at"]:
            setattr(state, key, val)
    storage.save()
    return jsonify(state.to_dict())
