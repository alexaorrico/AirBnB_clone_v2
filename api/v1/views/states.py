#!/usr/bin/python3
"""
Module state
route:
    - route states
"""

from api.v1.views import app_views
from flask import abort, jsonify
from models import storage
from flask import jsonify, abort, request
from models.state import State


#  Add views to app_views using the route decorator
@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """Retrieves the list of all State objects, use GET method"""
    data = storage.all(State).values()
    result = [obj.to_dict() for obj in data]

    return (jsonify(result))


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def states(state_id):
    """all object state"""
    state = storage.get(State, state_id)
    if (state is None):
        abort(404)
    result = state.to_dict()
    return jsonify(result)


@app_views.route('/states/<path:state_id>', methods=['DELETE'])
def delete(state_id):
    """Deletes a State object:: DELETE /api/v1/states/<state_id>"""
    delete_state = storage.get(State, state_id)
    if delete_state is None:
        abort(404)
    else:
        storage.delete(delete_state)
        storage.save()
        return (jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """Method that post a new state"""
    posted = request.get_json()
    if posted is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in posted:
        return (jsonify({'error': 'Mising name'}), 400)
    new_obj = State(**posted)
    new_obj.save()
    return jsonify(new_obj.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_states_id(state_id):
    ''' Update a State object, use PUT http method '''
    body = request.get_json()
    if body is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        ignore_key = ['id', 'created_at', 'updated_at']
        for key, value in body.items():
            if key not in ignore_key:
                setattr(state, key, value)
            else:
                pass
        state.save()
        return (jsonify(state.to_dict()), 200)
