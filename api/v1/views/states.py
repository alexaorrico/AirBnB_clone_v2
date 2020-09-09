#!/usr/bin/python3

"""
   States module
   View for State objects that handles all default RestFul API actions
"""
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import jsonify, request, make_response, abort


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """ Retrieves all the states stored """
    states = storage.all(State)
    out = [state.to_dict() for state in states.values()]
    return jsonify(out)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_a_state(state_id=None):
    """ Retrieves a state object according to its id """

    if state_id is None:
        return abort(404)
    my_state = storage.get(State, state_id)
    if my_state is not None:
        my_state = my_state.to_dict()
        return jsonify(my_state)

    return abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_a_state(state_id=None):
    """ Deletes a State object according to its id """

    if state_id is None:
        return abort(404)
    my_state = storage.get(State, state_id)
    if my_state is not None:
        storage.delete(my_state)
        storage.save()
        return make_response(jsonify({}), 200)

    return abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_a_state():
    """
        Creates a new State object according to
        the HTTP body request dictionary
    """
    body = request.get_json(silent=True)
    if body is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    if "name" not in body:
        return make_response(jsonify({'error': 'Missing name'}), 400)

    new = State(**body)
    new.save()
    return make_response(jsonify(new.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_a_state(state_id=None):
    """ Updates a state object according to its id """

    if state_id is None:
        return abort(404)

    my_state = storage.get(State, state_id)

    if my_state is not None:
        body = request.get_json(silent=True)
        if body is None:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        if 'id' in body:
            del body['id']
        if 'created_at' in body:
            del body['created_at']
        if 'updated_at' in body:
            del body['updated_at']
        my_state.__dict__.update(body)
        setattr(my_state, 'algo_mas', "funciona_no_jodaaaa!!!")
        my_state.save()

        return make_response(jsonify(my_state.to_dict()), 200)

    return abort(404)
