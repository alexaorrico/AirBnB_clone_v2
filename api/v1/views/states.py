#!/usr/bin/python3
"""
Define route for view State
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.state import State
from models import storage


@app_views.route('/states/<string:state_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
@app_views.route('/states', strict_slashes=False, methods=['GET', 'POST'])
def states(state_id=None):
    """Retrieves a State or All the States"""
    if request.method == 'GET':
        if state_id is not None:
            state = storage.get(State, state_id)
            if state is None:
                abort(404)
            return jsonify(state.to_dict())
        states = storage.all(State)
        states_dicts = [val.to_dict() for val in states.values()]
        return jsonify(states_dicts)

    elif request.method == 'DELETE':
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        storage.delete(state)
        storage.save()
        return make_response(jsonify({}), 200)

    elif request.method == 'POST':
        data = request.get_json()
        if not data:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        elif 'name' not in data:
            return make_response(jsonify({'error': 'Missing name'}), 400)
        else:
            state = State(**data)
            state.save()
            return make_response(jsonify(state.to_dict()), 201)

    elif request.method == 'PUT':
        state = storage.get(State, state_id)
        if state is None:
            abort(404)

        data = request.get_json()
        if not data:
            return make_response(jsonify({'error': 'not a json'}), 400)

        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, value)
        state.save()
        return make_response(jsonify(state.to_dict()), 200)
