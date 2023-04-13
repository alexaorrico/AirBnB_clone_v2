#!/usr/bin/python3
"""
create a new view that handles all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models import storage


@app_views.route('states', methods=['GET'], strict_slashes=False)
def get_all_state():
    """returns the list of all State objects"""
    # retrieve all objects registered in the State class
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in States])


@app_views.route('states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_id():
    """retrieves a State object using id"""
    # retrieve all objects registered in the State class
    states = storage.all(State)
    for key, value in states.items():
        # check if the state_id is linked to any State object
        if states[key].id == state_id:
            return value.to_dict()
    # if the state_id is not linkes to any State object raise an error
    abort(404)


@app_views.route('states/<state_id>', methods=['DELETE'], trict_slashes=False)
def delete_state():
    """delete a State object"""
    state = storage.get(State, state_id)
        
    #check if the state_id is linked to any State object, if not raise an error
    if state is None:
        abort(404)

    # delete a State object if the state_id is linked
    storage.delete(state)
    storage.save()

    # return an empty dictionary with the status code 200
    return (jsonify({}), 200)


@app_views.route('states', methods=['POST'], trict_slashes=False)
def post_state():
    """create a State"""
    # transform the HTTP body request to a dictionary
    items = request.get_json()

    # raise an error if the HTTP body request is not valid JSON
    if items is None:
        abort(400, 'NOT a JSON')

    # raise an error if the dictionary doesn’t contain the key name
    if 'name' not in items:
        abort(400, 'Missing name')

    # return the new State with the status code 201 
    new_state = State(**items)
    new_state.save()
    return (jsonify(new_state.to_dict()), 201)


@app_views.route('states/<state_id>', methods=['PUT'], trict_slashes=False)
def update_state():
    """update a State object"""
    state = storage.get(State, state_id)

    # raise an error if the state_id is not linked to any State object
    if state is None:
        abort(404)

    data = request.get_json()
    # raise an error if the HTTP body request is not valid JSON
    if data is None:
        abort(400, 'Not a JSON')

    ignore_keys = ['id', 'created_at', 'updated_at']

    # update the State object with all key-value pairs of the dictionary
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    state.save()

    #return the State object with the status code 200
    return (jsonify(state.to_dict()), 200)