#!/usr/bin/python3
"""
Create a new view that handles all default RESTFul API actions
get_all_state [GET]
get_state [GET]
delete_state [DELETE]
post_state [POST]
update_state [PUT]
"""
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_state():
    """returns HOW MANY DATA IN STORAGE"""
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app_views.route('states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_id(state_id):
    """retrieves a State object using id"""
    # retrieve all objects registered in the State class
    states = storage.all(State)
    for key, value in states.items():
        # check if the state_id is linked to any State object
        if states[key].id == state_id:
            return value.to_dict()
    # if the state_id is not linkes to any State object raise an error
    abort(404)


@app_views.route('states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """delete a State object"""

    state = storage.get(State, state_id)

    # check if the id is linked to any State object, if not raise an error
    if state is None:
        abort(404)

    # delete a State object if the state_id is linked
    storage.delete(state)
    storage.save()

    # return an empty dictionary with the status code 200
    return (jsonify({}), 200)


@app_views.route('states', methods=['POST'], strict_slashes=False)
def post_state():
    """create a State object"""
    items = request.get_json()

    if items is None:
        abort(400, 'Not a JSON')
        
    if 'name' not in items:
        abort(400, 'Missing name')

    new_state = State(**items)
    new_state.save()
    return (jsonify(new_state.to_dict()), 201)


@app_views.route('states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
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

    # return the State object with the status code 200
    return (jsonify(state.to_dict()), 200)
