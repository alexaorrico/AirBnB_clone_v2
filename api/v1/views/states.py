#!/usr/bin/python3
"""
Creates a new view for State objects for all default API actions
"""
from flask import request, jsonify, abort

from api.v1.views import app_views
from models import storage
from models.state import State


def getstate(state):
    """Get state"""
    if state is None:
        abort(404)
    return (jsonify(state.to_dict()), 200)


def putstate(state):
    """ Update state"""
    if state is None:
        abort(404)
    if not request.is_json:
        abort(400, 'Not a JSON')
    new = request.get_json()
    for (k, v) in new.items():
        if k is not 'id' and k is not 'created_at' and k is not 'updated_at':
            setattr(state, k, v)
    storage.save()
    return (jsonify(state.to_dict()), 200)


def deletestate(state):
    """Delete state"""
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/states', methods=['GET', 'POST'])
def states():
    """  Retrieves list of all state objs or creates a state"""
    if request.method == 'GET':
        all_states = [x.to_dict() for x in storage.all('State').values()]
        return (jsonify(all_states), 200)
    elif request.method == 'POST':
        if not request.is_json:
            abort(400, 'Not a JSON')
        new = request.get_json()
        if 'name' not in new.keys():
            abort(400, 'Missing name')
        x = State()
        for (k, v) in new.items():
            setattr(x, k, v)
        x.save()
        return (jsonify(x.to_dict()), 201)


@app_views.route('/states/<ident>', methods=['GET', 'PUT', 'DELETE'])
def states_id(ident):
    """Retrieves a specific state"""
    states = storage.all('State')
    for s in states.values():
        if s.id == ident:
            if request.method == 'GET':
                return getstate(s)
            elif request.method == 'PUT':
                return putstate(s)
            elif request.method == 'DELETE':
                return deletestate(s)
    abort(404, 'Not found')
