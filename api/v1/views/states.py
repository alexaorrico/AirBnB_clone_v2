#!/usr/bin/python3
"""Index view
"""
from api.v1.views import app_views
from flask import (
    abort,
    jsonify,
    make_response,
    request
)
from models import storage
from models.state import State


@app_views.route("/states", methods=['GET', 'POST'])
def states():
    """Retrieve all states or a state if <state_id> is provided
    """
    if request.method == 'GET':
        return jsonify([v.to_dict() for v in storage.all().values()])

    if request.method == 'POST':
        req = request.get_json()
        if req is None:
            abort(400, "Not a JSON")
        if 'name' not in req.keys():
            abort(400, "Missing name")
        state = State(**req)
        state.save()
        return make_response(state.to_dict(), 201)


@app_views.route("/states/<state_id>", methods=['GET', 'DELETE', 'PUT'])
def states_id(state_id=None):
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(state.to_dict())

    if request.method == 'DELETE':
        state.delete()
        storage.save()
        return jsonify({})

    if request.method == 'PUT':
        req = request.get_json()
        if req is None:
            abort(400, "Not a JSON")
        """
            Line 55-62 can be implemented in the
            base class to avoid repitition in other
            endpoints.
        """
        DEFAULTS = ['id', 'created_at', 'updated_at']
        new_dict = {
            k: v for k, v in req.items()
            if k not in DEFAULTS
        }
        for k, v in new_dict.items():
            setattr(state, k, v)
        state.save()
        return jsonify(state.to_dict())
