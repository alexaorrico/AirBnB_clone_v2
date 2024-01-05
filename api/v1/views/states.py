#!/usr/bin/python3
""" The  `app_views` blueprint for URI subpaths connected to `State` objects.
"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.state import State


@app_views.route("/states", methods=['GET'],
                 strict_slashes=False)
def GET_all_State():
    """ JSON list containing `State` instance that is stored

    Return:
        All instances of `State` in a JSON list
    """
    state_list = []
    for state in storage.all(State).values():
        state_list.append(state.to_dict())

    return jsonify(state_list)


@app_views.route("/states/<state_id>", methods=['GET'],
                 strict_slashes=False)
def GET_State(state_id):
    """ Returns the id of the `State` instance stored in URI subpath.

    Args:
        state_id: uuid of the stored `State` instance

    Return:
        404 error response or instance of `State` with matching uuid
    """
    state = storage.get(State, state_id)

    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route("/states/<state_id>", methods=['DELETE'],
                 strict_slashes=False)
def DELETE_State(state_id):
    """ Removes storage instance of `State` by id in URI subpath

    Args:
        state_id: uuid of `State` instance in storage

    Return:
        Responds 200 or 404 if error and an empty dictionary
    """
    state = storage.get(State, state_id)

    if state:
        storage.delete(state)
        storage.save()
        return ({})
    else:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def POST_State():
    """ Builds a fresh instance of `State` in storage

    Return:
        Responds 200 or 404 if error and an empty dictionary
    """
    req_dict = request.get_json()
    if not req_dict:
        return (jsonify({'error': 'Not a JSON'}), 400)
    elif 'name' not in req_dict:
        return (jsonify({'error': 'Missing name'}), 400)
    new_State = State(**req_dict)
    new_State.save()

    return (jsonify(new_State.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=['PUT'],
                 strict_slashes=False)
def PUT_State(state_id):
    """ updates the storage instance of `State` by using the
    id in URI subpath and kwargs from the HTTP body request.

    Args:
        state_id: the storage based uuid of `State` instance

    Return:
        Dictionary empty and response status 200, or 404 if
    an error
    """
    state = storage.get(State, state_id)
    req_dict = request.get_json()

    if state:
        if not req_dict:
            return (jsonify({'error': 'Not a JSON'}), 400)
        for key, value in req_dict.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, value)
        storage.save()
        return (jsonify(state.to_dict()))
    else:
        abort(404)
