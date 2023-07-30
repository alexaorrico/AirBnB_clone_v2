#!/usr/bin/python3
''' This module defines a view for State objects '''
from api.v1.views import state_views
from models import storage
from models.state import State
from flask import request, abort
import json


@state_views.route('/states', strict_slashes=False)
def get_states():
    ''' Retrives all state objects '''
    states = list(storage.all(State).values())
    json_rep = [state.to_dict() for state in states]
    return json.dumps(json_rep, indent=4)


@state_views.route('/states/<state_id>', strict_slashes=False)
def get_state(state_id):
    ''' Retrieves a state object '''
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return json.dumps(state.to_dict(), indent=4)


@state_views.route('/states/<state_id>', methods=['DELETE'],
                   strict_slashes=False)
def delete_state(state_id):
    ''' Deletes a state '''
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    state.delete()
    storage.save()

    return json.dumps({}, indent=4), 200


@state_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    ''' Adds a state '''
    try:
        data = request.get_json()
    except Exception:
        abort(400, description='Not a JSON')
    else:
        if 'name' not in data:
            abort(400, description='Missing name')
        state = State(**data)
        state.save()
        return json.dumps(state.to_dict(), indent=4), 201


@state_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    ''' Updates a state '''
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    try:
        data = request.get_json()
    except Exception:
        abort(400, description='Not a JSON')
    else:
        for key, value in data.items():
            if key in ['id', 'created_at', 'updated_at']:
                continue
            setattr(state, key, value)
        state.save()
        return json.dumps(state.to_dict(), indent=4), 200
