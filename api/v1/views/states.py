#!/usr/bin/python3
"""Module with the view for State objects"""
from api.v1.views import app_views
from models.state import State
from models import storage
from flask import request, abort
import json


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def states():
    """Return a list of dictionaries of all states"""
    if request.method == 'GET':
        states = []
        for state in storage.all(State).values():
            states.append(state.to_dict())
        return json.dumps(states, indent=4)
    try:
        data = request.get_json()
    except Exception:
        return 'Not a JSON', 400
    if 'name' not in data.keys():
        return 'Missing name', 400
    new_state = State(**data)
    new_state.save()
    return json.dumps(new_state.to_dict(), indent=4), 201



@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def states_id(state_id):
    if request.method == 'GET':
        for state in storage.all(State).values():
            if state.id == state_id:
                return json.dumps(state.to_dict(), indent=4)
        abort(404)
    if request.method == 'DELETE':
        state = storage.get(State, state_id)
        print(state)
        if state is not None:
            state.delete()
            storage.save()
            return {}
        abort(404)
    if request.method == 'PUT':
        state = storage.get(State, state_id)
        print(state)
        if state is None:
            abort(404)
        try:
            data = request.get_json()
        except Exception:
            return 'Not a JSON', 400
        for k, v in data.items():
            if k != 'id' or k != 'created_at' or k != 'updated_at':
                setattr(state, k, v)
        storage.save()
        return json.dumps(state.to_dict(), indent=4), 200

