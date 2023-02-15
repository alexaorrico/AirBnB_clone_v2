#!/usr/bin/python3
"""
handles all default RESTFUl API actions
"""

from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models import storage
from models.state import State
from models.engine.db_storage import classes


@app_views.route('/states', methods=['GET', 'POST'])
def all_states():
    """ defines route for api/v1/states """
    if request.method == 'GET':
        states = [state.to_dict() for state in storage.all('State').values()]
        return jsonify(states)

    if request.method == 'POST':
        if not request.json:
            return make_response('Not a JSON', 400)
        if 'name' not in request.json:
            return make_response('Missing name', 400)
        newObj = classes['State']
        newState = newObj(**request.json)
        newState.save()
        return jsonify(newState.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'])
def state_by_id(state_id):
    """ defines route for api/vi/states/<state_id> """
    if request.method == 'GET':
        state = [s for s in storage.all('State').values() if s.id == state_id]
        if (len(state) == 0):
            abort(404)
        return jsonify(state[0].to_dict())

    if request.method == 'DELETE':
        state = [s for s in storage.all("State").values() if s.id == state_id]
        if len(state) == 0:
            return make_response('Not found', 404)
        storage.delete(state[0])
        storage.save()
        return jsonify({})

    if request.method == 'PUT':
        state = [s for s in storage.all('State').values() if s.id == state_id]
        if len(state) == 0:
            abort(404)
        if not request.json:
            return make_response('Not a JSON', 400)
        data = request.json
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_ap']:
                setattr(state[0], key, value)
                state[0].save()
        return jsonify(state[0].to_dict()), 200
