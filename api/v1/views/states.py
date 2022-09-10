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
    states = storage.all("State")
    if request.method == 'DELETE':
        if state_id is not None:
            for value in states.values():
                if value.id == state_id:
                    storage.delete(value)
                    storage.save()
                    return {}, 200
            abort (404)
    elif request.method == 'POST':
        try:
            response = request.get_json()
            if 'name' in response.keys():
                new_state = State(**response)
                new_state.save()
                return new_state.to_dict(), 201
            else:
                abort (400, description="Missing name")
        except Exception:
            abort (400, description="Not a JSON")
        return test
    elif request.method == 'PUT':
        response = request.get_json()
        if type(response) is dict:
            response.pop("id", None)
            response.pop("created_at", None)
            response.pop("updated_at", None)
            for value in states.values():
                if value.id == state_id:
                    value.__dict__.update(response)
                    return value.to_dict(), 200
            abort (404)
        else:
            abort (400, description="Not a JSON")
    else:
        if state_id is not None:
            for value in states.values():
                if value.id == state_id:
                    return(jsonify(value.to_dict()))
            abort(404)
        else:
            states_list = []
            for value in states.values():
                states_list.append(value.to_dict())
            return jsonify(states_list)
