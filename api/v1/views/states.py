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


@app_views.route("/states", methods=['GET', 'POST'], strict_slashes=False)
def states():
    """Retrieve all states or a state if <state_id> is provided
    """
    if request.method == 'GET':
        return jsonify([v.to_dict() for v in storage.all(State).values()])

    if request.method == 'POST':
        req = request.get_json(silent=True)
        if req is None:
            abort(400, description="Not a JSON")
        if 'name' not in req.keys():
            abort(400, description="Missing name")
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
        req = request.get_json(silent=True)
        if req is None:
            abort(400, description="Not a JSON")
        state.update(req)
        return jsonify(state.to_dict())
