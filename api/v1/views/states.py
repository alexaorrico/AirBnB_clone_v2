#!/usr/bin/python3
"""states"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """ Retrieves the list of all State objects """
    states = storage.all("State")
    result = []
    for state in states.values():
        result.append(state.to_dict())
    return jsonify(result)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """fetches state object """
    states = storage.all("State")
    for key in states.keys():
        if key.split('.')[-1] == state_id:
            return jsonify(states.get(key).to_dict())
    abort(404)


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """del obj """
    states = storage.all("State")
    for key in states.keys():
        if key.split('.')[-1] == state_id:
            storage.delete(states.get(key))
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """creates obk """
    dic = request.get_json()
    if not dic:
        abort(400, "Not a JSON")
    if not ('name' in dic.keys()):
        abort(400, "Missing name")
    state = State(**dic)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """ obj update"""
    states = storage.all("State")
    state = None
    for key in states.keys():
        if key.split('.')[-1] == state_id:
            state = states.get(key)
    if not state:
        abort(404)
    new_dict = request.get_json()
    if not new_dict:
        abort(400, "Not a JSON")
    for key, value in new_dict.items():
        if key in ('id', 'created_at', 'updated_at'):
            continue
        else:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
