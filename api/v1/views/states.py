#!/usr/bin/python3
"""Handles all default RESTful API actions for State objects"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State

states_dict = storage.all(State)


@app_views.route('/states', methods=['GET'], strict_slashes=False,
                 endpoint='get_all_states')
def states():
    """Retrieves the list of all State objects"""

    all_states = []
    for value in states_dict.values():
        object_dict = value.to_dict()
        all_states.append(object_dict)

    return jsonify(all_states)


@app_views.route('/states/<state_id>', methods=['GET'],
                 strict_slashes=False, endpoint='get_state')
def get_a_state(state_id):
    """Retrieves a State object with a unique id"""
    # for value in states_dict.values():
    #     object_dict = value.to_dict()
    #     if object_dict['id'] == state_id:
    #         return jsonify(object_dict)

    obj = storage.get(State, state_id)
    if obj is not None:
        object_dict = obj.to_dict()
        return jsonify(object_dict)

    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False, endpoint='delete_state')
def delete(state_id):
    """Deletes a State object using its id"""
    the_obj = storage.get(State, state_id)

    if the_obj is not None:
        storage.delete(the_obj)
        storage.save()

        return jsonify({}), 200

    abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False,
                 endpoint='create_state')
def create_state():
    """Creates a new State object"""
    try:
        received = request.get_json()
    except Exception:
        abort(400, description='Not a JSON')

    if 'name' not in received:
        abort(400, description='Missing name')

    new_state = State(**request)

    # new_state.name = received['name']
    storage.new(new_state)
    storage.save()

    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False, endpoint='update_state')
def update_state(state_id):
    """Updates a State object given its id"""
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    try:
        received = request.get_json()
    except Exception:
        abort(400, description='Not a JSON')

    for key, value in received.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)

    state.save()
    storage.save()

    return jsonify(state.to_dict()), 200


# @app_views.errorhandler(400)
# def response_not_json(err):
#     """Handles 400 errors and displays custom message"""
#     return make_response(jsonify({'error': err.description}), 400)
