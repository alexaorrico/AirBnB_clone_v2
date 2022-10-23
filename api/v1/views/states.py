#!/usr/bin/python3
"""Module state.py: starts all routes with `state`"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.state import State
from models import storage


@app_views.route('/states',
                 methods=['GET', 'POST'],
                 strict_slashes=False)
def states():
    """returns all state object"""
    if request.method == 'POST':
        response = request.get_json()

        if response is None:
            abort(400, description='Not a JSON')

        if 'name' not in list(response.keys()):
            abort(400, description='Missing name')
        new_state = State(**response)
        new_state.save()
        return(new_state.to_dict()), 201

    objs = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(objs)


@app_views.route('/states/<state_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def state(state_id):
    """returns a state based on the id"""

    for state in storage.all(State).values():

        if state.id == state_id:

            if request.method == 'DELETE':
                state.delete()
                storage.save()
                return '{}'

            if request.method == 'PUT':
                response = request.get_json()
                if response is None:
                    abort(400, description='Not a JSON')
                for k, v in response.items():
                    if k.endswith('ated_at') or k == 'id':
                        continue
                    setattr(state, k, v)
                state.save()
                
            return jsonify(state.to_dict())

    abort(404)
