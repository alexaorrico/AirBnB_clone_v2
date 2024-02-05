#!/usr/bin/python3
"""
Define route for view State
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.state import State
from models import storage

@app_views.route('/states/<string:state_id>', strict_slashes=False, methods=['GET', 'DELETE'])
@app_views.route('/states', strict_slashes=False)
def get_states(state_id=None):
    """Retrieves a State or All the States"""
    if request.method == 'GET':
        if state_id is not None:
            state = storage.get(State, state_id)
            if state is None:
                abort(404)
            return jsonify(state.to_dict())
        states = storage.all(State)
        states_dicts = [val.to_dict() for val in states.values()]
        return jsonify(states_dicts)
    elif request.method == 'DELETE':
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        storage.delete(state)
        storage.save()
        return make_response(jsonify({}), 200)

