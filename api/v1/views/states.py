#!/usr/bin/python3
"""
Define route for view State
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models import storage


@app_views.route('/states/<string:state_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
@app_views.route('/states', strict_slashes=False, methods=['GET', 'POST'])
def states(state_id=None):
    """Retrieves, Update, Create and Delete State or All the States"""
    state = storage.get(State, state_id)

    if request.method == 'GET':
        if state_id is not None:
            if state is None:
                abort(404)
            return jsonify(state.to_dict())
        states = storage.all(State)
        states_dicts = [val.to_dict() for val in states.values()]
        return jsonify(states_dicts)

    if request.method == 'POST':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        if 'name' not in data:
            abort(400, 'Missing name')
        state = State(**data)
        state.save()
        return jsonify(state.to_dict()), 201

    if state is None:
        abort(404)

    if request.method == 'DELETE':
        storage.delete(state)
        storage.save()
        return jsonify({})

    if request.method == 'PUT':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')

        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, value)
        state.save()
        return jsonify(state.to_dict())
