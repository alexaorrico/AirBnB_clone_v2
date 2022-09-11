#!/usr/bin/python3
"""variable app_views which is an instance of Blueprint"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states/', methods=['GET', 'POST'])
@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'])
def states(state_id=None):
    """retrieves an objects into a valid JSON"""
    if request.method == 'DELETE':
        if state_id is not None:
            state = storage.get(State, state_id)
            if state is not None:
                storage.delete(state)
                storage.save()
                return {}, 200
            else:
                abort (404)
    elif request.method == 'POST':
        response = request.get_json()
        if type(response) is dict:
            if 'name' in response:
                new_state = State(**response)
                new_state.save()
                return jsonify(new_state.to_dict()), 201
            else:
                abort (400, description="Missing name")
        else:
            abort (400, description="Not a JSON")
        return test
    elif request.method == 'PUT':
        response = request.get_json()
        if type(response) is dict:
            state = storage.get(State, state_id)
            if state is not None:
                response.pop("id", None)
                response.pop("created_at", None)
                response.pop("updated_at", None)
                for key, value in response.items():
                    setattr(state, key, value)
                state.save()
                return jsonify(state.to_dict()), 200
            else:
                abort (404)
        else:
            abort (400, description="Not a JSON")
    else:
        if state_id is not None:
            state = storage.get(State, state_id)
            if state is not None:
                return(jsonify(state.to_dict()))
            else:
                abort(404)
        else:
            states = storage.all("State")
            states_list = []
            for value in states.values():
                states_list.append(value.to_dict())
            return jsonify(states_list)
