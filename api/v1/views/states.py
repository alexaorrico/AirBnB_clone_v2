#!/usr/bin/python3
"""
    This is the states page handler for Flask.
"""
from api.v1.views import app_views
from models import storage
from flask import abort, jsonify, request

from models.state import State


@app_views.route('/states', methods=['GET', 'POST'])
def states():
    """
        Flask route at /states.
    """
    if request.method == 'POST':
        kwargs = request.get_json()
        if not kwargs:
            return {"error": "Not a JSON"}, 400
        if "name" not in kwargs:
            return {"error": "Missing name"}, 400
        new_state = State(**kwargs)
        new_state.save()
        return new_state.to_dict(), 201

    elif request.method == 'GET':
        return jsonify([o.to_dict() for o in storage.all("State").values()])


@app_views.route('/states/<id>', methods=['GET', 'DELETE', 'PUT'])
def states_id(id):
    """
        Flask route at /states/<id>.
    """
    state = storage.get(State, id)
    if (state):
        if request.method == 'DELETE':
            state.delete()
            storage.save()
            return {}, 200

        elif request.method == 'PUT':
            kwargs = request.get_json()
            if not kwargs:
                return {"error": "Not a JSON"}, 400
            for k, v in kwargs.items():
                if k not in ["id", "created_at", "updated_at"]:
                    setattr(state, k, v)
            state.save()
        return state.to_dict()
    abort(404)
