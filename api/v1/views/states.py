#!/usr/bin/python3

""" Handles all restful API actions for State"""

from api.v1.views import app_views
from flask import request, jsonify, abort
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """ Returns all states to the mapped URL """
    state_objs = storage.all(State)
    states = [obj.to_dict() for obj in state_objs.values()]
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'],
                 strict_slashes=False)
def get_individual_states(state_id):
    """" Returns indivuidual states by id """
    state_objs = storage.all(State)
    states = [obj.to_dict() for obj in state_objs.values()]

    for state in states:
        if state.get('id') == state_id:
            return jsonify(state)
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ Deletes individual states by id """
    state = storage.get(State, state_id)

    if state is None:
        abort(404)
    """ Retrieve all the cities associated with the state"""
    cities = state.cities

    """ Delete the assciated cities """
    """ We have to delete the cites first before deleting the state
        The State id is a foreign key in the Cities table
        If we delete the cities before the state, the state id
        will be null in the cities table. This will break the rules
        of SQL and return an error. To counter this, we delete the
        cities associated with the states firs, then the states"""
    for city in cities:
        storage.delete(city)

    """ Delete the state """
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_states():
    """ Creates a state by using the URL """
    my_dict = request.get_json()

    if my_dict is None:
        abort(400, 'Not a JSON')
    if my_dict.get("name") is None:
        abort(400, 'Missing name')
    new_state = State(**my_dict)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """ Updates a state by state ID """
    state_objs = storage.all(State)

    my_dict = request.get_json()

    if my_dict is None:
        abort(400, 'Not a JSON')
    for state in state_objs.values():
        if state.id == state_id:
            state.name = my_dict.get("name")
            state.save()
            return jsonify(state.to_dict()), 200
    abort(404)
