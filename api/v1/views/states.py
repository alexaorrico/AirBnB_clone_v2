#!/usr/bin/python3
"""View states"""

import models
from models.state import State
from flask import jsonify, abort
from flask import request as req
from api.v1.views import app_views


@app_views.route('/states', methods=['GET', 'POST'])
def statesAll():
    """Retrieves the list of all State objects"""
    if req.method == 'GET':
        states = models.storage.all('State')
        states = [st.to_dict() for st in states.values()]
        return jsonify(states)

    if req.method == 'POST':
        body = req.get_json()
        if body is None:
            abort(400, 'Not a JSON')
        if body.get('name', None) is None:
            abort(400, 'Missing name')
        state = State(**body)
        state.save()
        return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['GET', 'PUT', 'DELETE'])
def stateId(state_id):
    """id state retrieve json object"""
    state = models.storage.get('State', state_id)
    if state is None:
        abort(404)

    if req.method == 'GET':
        return jsonify(state.to_dict())

    if req.method == 'PUT':
        state_json = req.get_json()
        if state_json is None:
            abort(400, 'Not a JSON')
        ignore = ['id', 'created_at', 'updated_at']
        for key, val in state_json.items():
            if key not in ignore:
                setattr(state, key, value)
        models.storage.save()
        return jsonify(state.to_dict())

    if req.method == 'DELETE':
        state.delete()
        models.storage.save()
        return jsonify({})
