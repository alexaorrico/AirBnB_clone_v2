#!/usr/bin/python3
""" CRUD operation on state object"""
from models.state import State
from api.v1.views import app_views
from models import storage
from flask import jsonify
from flask import abort, request


@app_views.route('/states', methods=['GET'])
def all_states():
    """
    The function `all_states` retrieves all instances of the
    `State` class from storage and returns them as a JSON list."""
    all_state = storage.all(State)
    my_list = []
    for i in all_state.values():
        my_list.append(i.to_dict())
    return jsonify(my_list)


@app_views.route('/states/<id>')
def states_id(id: str):
    """
    The function `states_id` takes an ID as input and returns the
    corresponding state object as a JSON response, or raises a
    404 error if the state is not found.
    """
    all_state = storage.all(State)
    for i in all_state.values():
        if i.id == id:
            return jsonify(i.to_dict())
    abort(404)


@app_views.route('/states/<id>', methods=['DELETE'])
def states_id_delete(id: str):
    """
    The function `states_id_delete` deletes a state
    object from storage based on its ID.
    """
    all_state = storage.all(State)
    for i in all_state.values():
        if i.id == id:
            storage.delete(i)
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def states_post():
    """
    The function `states_post()` receives a JSON object,
    checks if it is valid, creates a new State object,
    saves it to storage, and returns the State object as a JSON response.
    """
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if 'name' not in data.keys():
        abort(400, "Missing name")
    state = State(**data)
    storage.new(state)
    storage.save()
    return jsonify(storage.get(State, state.id).to_dict())


@app_views.route('states/<id>', methods=['PUT'])
def states_put(id: str):
    """
    The function updates the attributes of a state object based
    on the provided JSON data and returns the updated state
    object as a JSON response."""
    state = storage.get(State, id)
    if state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if 'id' in data.keys():
        del data['id']
    if 'created_at' in data.keys():
        del data['created_at']
    if 'updated_at' in data.keys():
        del data['updated_at']
    for i, j in data.items():
        setattr(state, i, j)
    storage.save()
    return jsonify(storage.get(State, state.id).to_dict())
