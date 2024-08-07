#!/usr/bin/python3
'''states module'''

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def getStates(state_id=None):
    '''gets all states or state with their id passed'''
    if state_id is None:
        result = []
        states = storage.all(State)
        for state in states.values():
            result.append(state.to_dict())
        return jsonify(result)

    result = storage.get(State, state_id)
    if res is None:
        abort(404)
    return jsonify(result.to_dict())


@app_views.route('/states/<state_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def deleteState(state_id=None):
    '''deletes a state'''
    if state_id is not None:
        result = storage.get(State, state_id)
        if result is not None:
            storage.delete(result)
            storage.save()
            return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def postState():
    '''posts a new state'''
    body = request.get_json()
    if body is None or type(body)is not dict:
        abort(400, description='Not a JSON')
    if 'name' not in body.keys():
        abort(400, description='Missing name')
    obj = State(**body)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def updateState(state_id=None):
    '''updates a state'''
    if state_id is None:
        abort(404)
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)

    body = request.get_json()
    if body is None:
        abort(400, 'Not a JSON')
    for key in body.keys():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(obj, key, body[key])
    obj.save()
    return make_response(jsonify(obj.to_dict()), 200)
