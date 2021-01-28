#!/usr/bin/python3
"""handles state route requests"""
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, request, abort


@app_views.route('/states', strict_slashes=False, methods=['POST', 'GET'])
@app_views.route('/states/<state_id>', strict_slashes=False, methods=[
    'PUT', 'GET', 'DELETE'])
def states(state_id=None):
    """retrieves list of all states or state by state_id"""
    if state_id is None:
        # /states GET method
        if request.method == 'GET':
            list_states = []
            for state in storage.all('State').values():
                list_states.append(state.to_dict())
            return jsonify(list_states)

        # /states POST method
        if request.method == 'POST':
            new_json = request.get_json(silent=True)
            if new_json is None:
                abort(400, 'Not a JSON')
            if 'name' not in new_json:
                abort(400, 'Missing name')
            new = State(**new_json)
            new.save()
            return jsonify(new.to_dict()), 201

    else:
        # /states/<state_id> GET method
        if request.method == 'GET':
            for state in storage.all('State').values():
                if state.id == state_id:
                    return jsonify(state.to_dict())
            abort(404)

        # /states/<state_id> DELETE method
        if request.method == 'DELETE':
            for state in storage.all('State').values():
                if state.id == state_id:
                    state.delete()
                    storage.save()
                    return jsonify({}), 200
            abort(404)

        # /states/<state_id> PUT method
        if request.method == 'PUT':
            for state in storage.all('State').values():
                if state.id == state_id:
                    new_json = request.get_json(silent=True)
                    if new_json is None:
                        abort(400, 'Not a JSON')
                    for k, v in new_json.items():
                        setattr(state, k, v)
                    state.save()
                    return jsonify(state.to_dict()), 200
            abort(404)
