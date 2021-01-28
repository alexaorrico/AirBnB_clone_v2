#!/usr/bin/python3
""" a new view for State objects that handles all default RestFul API actions
"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State


@app_views.route('/states/', methods=['GET'], strict_slashes=False)
def states_get():
    """retrieves the list of all State objects
    """
    states = storage.all("State").values()
    json_states = jsonify([state.to_dict() for state in states])
    return json_states


@app_views.route('/states/<state_id>/', methods=['GET'], strict_slashes=False)
def states_get_error(state_id):
    """retrieves a State object
    """
    try:
        state = jsonify(storage.get('State', state_id).to_dict())
        return state
    except:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_states(state_id):
    """deletes a State object
    """
    state = storage.get('State', state_id)
    if state is None:
        return jsonify(abort(404))
    state.delete()
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def post_state():
    """creates a state
    """
    info = request.get_json()
    if info is None:
        return jsonify(abort(400, 'Not a JSON'))

    name = info.get('name')
    if name is None:
        return jsonify(abort(400, 'Missing name'))

    state_post = State(**info)
    state_post.save()

    return (jsonify(state_post.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_states(state_id):
    """updates a state object
    """
    info = request.get_json()
    if info is None:
        return jsonify(abort(400, 'Not a JSON'))

    state_info = storage.get("State", state_id)
    if state_info is None:
        abort(404)

    ignore_keys = ["id", "created_at", "updated_at"]
    for key, value in info.items():
        if key not in ignore keys:

    state_info.save()
    return jsonify(state_info.to_dict())
