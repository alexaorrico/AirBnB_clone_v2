#!/usr/bin/python3
'''View to handle the RESTful API actions for 'State' objects'''
from flask import jsonify, request, abort

from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def states():
    '''Handles "/states" route'''
    if request.method == 'GET':
        states = [state.to_dict() for state in storage.all(State).values()]
        return jsonify(states)

    if request.method == 'POST':
        data = request.get_json()
        if data is None or type(data) is not dict:
            return 'Not a JSON', 400
        name = data.get('name')
        if name is None:
            return 'Missing name', 400
        state = State(**data)
        state.save()
        return jsonify(state.to_dict()), 201


@app_views.route('/states/<string:state_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def state_actions(state_id):
    '''Handles actions for "/states/<state_id>" route'''
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(state.to_dict())

    if request.method == 'DELETE':
        storage.delete(state)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        data = request.get_json()
        if data is None or type(data) is not dict:
            return 'Not a JSON', 400
        for attr, val in data.items():
            if attr not in ['id', 'created_at', 'updated_at']:
                setattr(state, attr, val)
        state.save()
        return jsonify(state.to_dict()), 200
