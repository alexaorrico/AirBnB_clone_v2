#!/usr/bin/python3

"""
This module is for State objects that handles all
default RESTFul API actions
"""
from models.state import State
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """
    states get the list of all state objects
    """
    obj = storage.all(State)
    lis = []
    for key, value in obj.items():
        st = obj[key]
        lis.append(st.to_dict())
    return jsonify(lis)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def states_obj(state_id):
    """
    Get's object of State using id e.g (8f165686-c98d-46d9-87d9-d6059ade2d99)
    """
    obj = storage.all(State)
    try:
        for key, value in obj.items():
            if value.id == state_id:
                return jsonify(value.to_dict())
        abort(404)
    except Exception:
        abort(404)


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_state(state_id):
    """
    DELETE State with id (state_id)
    """
    obj = storage.all(State)
    try:
        for key, value in obj.items():
            if value.id == state_id:
                storage.delete(value)
                storage.save()
                empty = {}
                return jsonify(empty), 200
        abort(404)
    except Exception:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """
    POST to State with body or content of request
    """

    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    elif not data.get('name'):
        abort(400, description="Missing name")
    else:
        new_obj = State()
        new_obj.name = data.get('name')
        storage.new(new_obj)
        storage.save()
        return jsonify(new_obj.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """
    PUT to update State with body or content of request
    """
    data = request.get_json()

    # Check if JSON is provided
    if data is None:
        abort(400, description="Not a JSON")

    # Retrieve the state object by ID
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    # Update state object with provided data
    for name, val in data.items():
        if name not in ('id', 'created_at', 'updated_at'):
            setattr(state, name, val)

    # Save changes to the storage
    storage.save()

    return jsonify(state.to_dict()), 200
