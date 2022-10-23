#!/usr/bin/python3
"""states view module that handles
all default API actions"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET', POST], strict_slashes=False)
def states():
    if request.method == 'GET':
        states_obj = storage.all('State')
        states_obj = [obj.to_dict() for obj in states_obj.values()]
        return jsonify(states_obj)
    if request.method == 'POST':
        req_body = request.get_json()
        if req_body is None:
            abort(400, 'Not a JSON')
        if req_body.get('name') is None:
            abort(400, 'Missing name')
        new_state = State(**req_body)
        new_state.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def a_state(state_id=None):
    """ handles /states/<state_id> route"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404, 'Not found')
    if request.method == 'GET':
        return jsonify(state.to_dict())
    if request.method == 'DELETE':
        state.delete()
        del state
        return jsonify({})
    if request.method == 'PUT':
        req_body = request.get_json()
        if req_body is None:
            abort(400, 'Not a JSON')
        state.update(req_body)
        return jsonify(state.to_dict())
