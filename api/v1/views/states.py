#!/usr/bin/python3
"""RESTful API action for State object"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route('/states')
@app_views.route('/states/<state_id>')
def state_get(state_id=None):
    """
    get all states or a state if state_id is specified
    """
    if state_id:
        state = storage.get(State, state_id)
        if state:
            return jsonify(state.to_dict())
        else:
            abort(404)
    else:
        states = storage.all(State).values()
        states = [state.to_dict() for state in states]
        return jsonify(states)


@app_views.route('/states/<state_id>', methods=["DELETE"])
def state_delete(state_id):
    """
    delete method handler.
    will delete a state with the specified id.
    """
    state = storage.get(State, state_id)

    if state:
        storage.delete(state)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route('/states', methods=['POST'])
def state_post():
    """
    route handler for creating a new state
    """
    if not request.is_json:
        return "Not a JSON", 400
    data = request.get_json()
    if data.get('name') is None:
        return "Missing name", 400
    name = data.get('name')
    state = State()
    state.name = name
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def state_put(state_id):
    """
    route handler for updating a state
    """
    if not request.is_json:
        return "Not a JSON", 400
    data = request.get_json()
    state = storage.get(State, state_id)

    if state is None:
        return abort(404)

    for key, value in data.items():
        if key in ('id', 'created_at', 'updated_at'):
            continue
        else:
            setattr(state, key, value)

    state.save()
    return jsonify(state.to_dict()), 200
