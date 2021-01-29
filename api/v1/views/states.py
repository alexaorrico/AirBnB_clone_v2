#!/usr/bin/python3
"""new view for State objects that handles all
default RestFul API actions
"""
from flask import Flask, jsonify, make_response, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", methods=['GET'], strict_slashes=False)
@app_views.route("/states/<state_id>", methods=['GET'], strict_slashes=False)
def state_view(state_id=None):
    """
    Retrieves the list of all State objects
    """
    if state_id:
        st = storage.get(State, state_id)
        if st is None:
            abort(404)
        return jsonify(st.to_dict())
    else:
        states = [value.to_dict() for value in storage.all(State).values()]
        return jsonify(states)


@app_views.route(
    "/states/<state_id>", methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object"""
    st = storage.get(State, state_id)
    if st is None:
        abort(404)
    storage.delete(st)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states", methods=['POST'], strict_slashes=False)
def post_state():
    """Create a State"""
    content = request.get_json()
    if content:
        if content.get('name'):
            new_state = State(**content)
            new_state.save()
            return jsonify(new_state.to_dict()), 201
        abort(400, "Missing name")
    else:
        abort(400, "Not a JSON")


@app_views.route("/states/<state_id>", methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a State object"""
    st = storage.get(State, state_id)
    if st is None:
        abort(404)
    else:
        content = request.get_json()
        if content:
            keys_ignored = ['id', 'created_at', 'updated_at']
            for key, value in content.items():
                if key not in keys_ignored:
                    setattr(st, key, value)
            st.save()
            return jsonify(st.to_dict()), 200
        else:
            abort(400, "Not a JSON")
