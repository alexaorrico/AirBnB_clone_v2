#!/usr/bin/python3
"""
Imports
"""
from models.state import State
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage


"""
Def GET method
"""


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def getstatelist():
    """
    Return State list
    """
    states = []
    states_list = storage.all(State)
    states_list = [state.to_dict() for state in states.values()]
    return jsonify(states_list)


"""
Def GET method
"""


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def getstate1(state_id):
    """
    Return 404 if there is not a state object
    """
    state = State.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(storage.get(State, state_id).to_dict())


"""
Def delete method
"""


@app_views.route('/states/<state_id>', methods=['DELETE'])
def deletestate(state_id):
    """
    Delete state by id
    """
    state = State.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(states)
    storage.save()
    return {

    }, 200


"""
Def POST method
"""


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def create_state():
    """
    Create a new State
    """
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    new_state = State(**data)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


"""
Def PUT method
"""


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put(self, state_id):
    """
    Delete a state by id
    """
    state = State.query.get(state_id)
    if state is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')

    ignored_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(state, key, value)

    db.session.commit()
    return jsonify(state.to_dict()), 200
